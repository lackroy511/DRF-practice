from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email', 'password', 'first_name', 'last_name', 'is_staff',
            'is_active', 'date_joined', 'payments',
        )

    payments = PaymentSerializer(many=True)


class OtherUserRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email', 'first_name', 'is_staff', 'is_active', 'date_joined',
        )


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls,  user):
        token = super().get_token(user)

        token['email'] = user.email

        return token
