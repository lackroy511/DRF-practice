
import os

import stripe
from django.shortcuts import redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from course.permissions import IsCurrentUser
from users.models import Payment, Subscription, User
from users.serializers import (MyTokenObtainPairSerializer,
                               OtherUserRetrieveSerializer,
                               PaymentCreateSerializer, PaymentSerializer,
                               SubscriptionSerializer, UserRetrieveSerializer,
                               UserSerializer)
from users.services import (get_session_of_payment,
                            get_payment_info,
                            save_serializer)


class UserCreateAPIView(generics.CreateAPIView):

    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        new_user = serializer.save()
        new_user.set_password(new_user.password)
        new_user.save()


class UserUpdateAPIView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsCurrentUser, )


class UserRetrieveAPIView(generics.RetrieveAPIView):

    # serializer_class = UserRetrieveSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.user == self.get_object():
            return UserRetrieveSerializer

        return OtherUserRetrieveSerializer


class PaymentsListAPIView(generics.ListAPIView):

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = (DjangoFilterBackend, OrderingFilter)

    filterset_fields = ('paid_lesson', 'paid_course', 'method')
    ordering_fields = ('date_of_payment', )


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentCreateSerializer
    
    def perform_create(self, serializer):
        session = get_session_of_payment(self)
        save_serializer(self, session, serializer)


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    
    def get_object(self):
        payment = super().get_object()
        
        if payment.status != 'complete':
            stripe_data = get_payment_info(payment.stripe_payment_id)
            payment.status = stripe_data.get('status')
            payment.save()

        return payment


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]
