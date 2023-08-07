from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter

from users.models import Payment, User
from users.serializers import (PaymentSerializer, UserRetrieveSerializer,
                               UserSerializer)


class UserUpdateAPIView(generics.UpdateAPIView):

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(generics.RetrieveAPIView):

    serializer_class = UserRetrieveSerializer
    queryset = User.objects.all()


class PaymentsListAPIView(generics.ListAPIView):

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = (DjangoFilterBackend, OrderingFilter)

    filterset_fields = ('paid_lesson', 'paid_course', 'method')
    ordering_fields = ('date_of_payment',)
