from django.contrib import admin

from users.models import Payment, User

# Register your models here.


admin.site.register(User)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('date_of_payment', 'amount')
