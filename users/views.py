
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from course.permissions import IsCurrentUser
from users.models import Payment, Subscription, User
from users.serializers import (MyTokenObtainPairSerializer,
                               OtherUserRetrieveSerializer, PaymentSerializer,
                               SubscriptionSerializer, UserRetrieveSerializer,
                               UserSerializer)


class UserCreateAPIView(generics.CreateAPIView):

    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        new_user = serializer.save()
        new_user.set_password(new_user.password)
        new_user.save()

        # password = serializer.validated_data['password']
        # hashed_password = make_password(password)
        # serializer.save(password=hashed_password)


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


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
