from course.models import Course, Lesson

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    username = None
    email = models.EmailField(
        unique=True, verbose_name='почта',
    )

    def __str__(self):
        return f'{self.email}'


class Payment(models.Model):

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ('-date_of_payment',)

    CASH = 'cash'
    TRANSFER = 'transfer'

    METHOD_CHOICES = (
        (CASH, 'наличные'),
        (TRANSFER, 'перевод'),
    )

    date_of_payment = models.DateTimeField(
        auto_now_add=True,
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Сумма платежа',
    )
    method = models.CharField(
        max_length=50, choices=METHOD_CHOICES,
    )
    paid_lesson = models.ForeignKey(
        Lesson, verbose_name='Оплаченный урок', on_delete=models.CASCADE,
        null=True, blank=True, related_name='paid_lessons',
    )
    paid_course = models.ForeignKey(
        Course, verbose_name='Оплаченный курс', on_delete=models.CASCADE,
        null=True, blank=True, related_name='paid_courses',
    )
    user = models.ForeignKey(
        User, verbose_name='пользователь', on_delete=models.CASCADE,
        related_name='payments',
    )
