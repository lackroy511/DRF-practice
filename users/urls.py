from django.urls import path

from users.apps import UsersConfig
from users.views import (MyTokenObtainPairView, PaymentsListAPIView,
                         UserCreateAPIView, UserRetrieveAPIView,
                         UserUpdateAPIView)

app_name = UsersConfig.name

urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name='create-user'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='update-user'),
    path('detail/<int:pk>/', UserRetrieveAPIView.as_view(), name='user-detail'),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('payments/', PaymentsListAPIView.as_view(), name='user-payments'),
]
