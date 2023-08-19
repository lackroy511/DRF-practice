from django.contrib import admin

from users.models import Payment, Subscription, User

# Register your models here.


# admin.site.register(User)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'date_of_payment', 'stripe_payment_id', 'amount')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'course', 'user')
