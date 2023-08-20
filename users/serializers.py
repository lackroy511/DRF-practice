from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import Payment, Subscription, User
from users.validators import AlreadySubscribedCheck

from datetime import date


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = (
            'pk', 'date_of_payment', 'amount', 'paid_lesson', 'paid_course', 'user',
            'stripe_payment_id', 'stripe_payment_url', 'method', 'status',
        )
        

class PaymentCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Payment
        fields = ('amount', 'paid_lesson', 'paid_course', 'stripe_payment_id', 'stripe_payment_url')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email', 'password', 'first_name', 'last_name', 'is_staff',
            'is_active', 'date_joined', 'last_login', 'payments',
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
        
        user.last_login = date.today()
        user.save()

        return token


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('course', 'user', 'course_name')
        validators = [AlreadySubscribedCheck()]
