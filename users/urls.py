from django.urls import path

from users.apps import UsersConfig
from users.views import (MyTokenObtainPairView, PaymentCreateAPIView,
                         PaymentRetrieveAPIView, PaymentsListAPIView,
                         SubscriptionCreateAPIView, SubscriptionDestroyAPIView,
                         UserCreateAPIView, UserRetrieveAPIView,
                         UserUpdateAPIView)

app_name = UsersConfig.name

urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name='create-user'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='update-user'),
    path('detail/<int:pk>/', UserRetrieveAPIView.as_view(), name='user-detail'),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('payment/', PaymentsListAPIView.as_view(), name='user-payment'),
    path('payment/create/', PaymentCreateAPIView.as_view(), name='user-payment-create'),
    path('payment/detail/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='user-payment-detail'),
    
    path('sub/create/', SubscriptionCreateAPIView.as_view(), name='user-sub-create'),
    path('sub/delete/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='user-sub-delete'),
]
