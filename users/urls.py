from django.urls import path

from users.apps import UsersConfig
from users.views import PaymentsListAPIView, UserRetrieveAPIView, \
    UserUpdateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path("update/<int:pk>/", UserUpdateAPIView.as_view(), name="update-user"),
    path("detail/<int:pk>/", UserRetrieveAPIView.as_view(), name="user-detail"),

    path("payments/", PaymentsListAPIView.as_view(), name="user-payments"),
]
