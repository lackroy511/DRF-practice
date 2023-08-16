
import os
from django.shortcuts import redirect

import stripe
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from course.models import Course, Lesson
from course.permissions import IsCurrentUser
from users.models import Payment, Subscription, User
from users.serializers import (MyTokenObtainPairSerializer,
                               OtherUserRetrieveSerializer,
                               PaymentCreateSerializer, PaymentSerializer,
                               SubscriptionSerializer, UserRetrieveSerializer,
                               UserSerializer)


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
        
        stripe.api_key = os.getenv('STRIPE_TOKEN')

        amount = self.request.data.get('amount')
        paid_lesson_id = self.request.data.get('paid_lesson')
        paid_course_id = self.request.data.get('paid_course')
        
        paid_obj = None
        if paid_course_id:
            paid_obj = Course.objects.get(pk=paid_course_id)
        elif paid_lesson_id:
            paid_obj = Lesson.objects.get(pk=paid_lesson_id)
        
        if paid_obj:
            stripe_product = stripe.Product.create(
                name=paid_obj.name,
            )
        
            stripe_price = stripe.Price.create(
                unit_amount=amount * 100,
                currency='rub',
                product=stripe_product.stripe_id,
            )
            
            line_items = {
                'price': stripe_price.stripe_id,
                'quantity': 1,
            }
            
            session = stripe.checkout.Session.create(
                success_url='https://example.com/success',
                line_items=[
                    line_items,
                ],
                mode='payment',
            )
            
            serializer.save(
                stripe_payment_id=session.get('id'),
                stripe_payment_url=session.get('url'),
                status=session.get('status'),
                user=self.request.user,
                method=Payment.TRANSFER,
            )


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    
    def get_object(self):
        payment = super().get_object()
        
        stripe.api_key = os.getenv('STRIPE_TOKEN')
        stripe_data = stripe.checkout.Session.retrieve(
            payment.stripe_payment_id,
        )
        
        payment.status = stripe_data.get('status')
        payment.save
        
        return payment


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
