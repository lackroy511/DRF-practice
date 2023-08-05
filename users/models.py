from django.db import models
from django.contrib.auth.models import AbstractUser

from course.models import Course
from lesson.models import Lesson

# Create your models here.


class User(AbstractUser):

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    def __str__(self):
        return f'{self.email}'


class Payment(models.Model):

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    date_of_payment = models.DateTimeField(
        auto_now_add=True,
    )
    user = models.ForeignKey(
        User, verbose_name='пользователь', on_delete=models.CASCADE,
    )
    paid_course = models.ForeignKey(
        Course, verbose_name='Оплаченный курс', on_delete=models.CASCADE,
        null=True, blank=True,
    )
    paid_lesson = models.ForeignKey(
        Lesson, verbose_name='Оплаченный урок', on_delete=models.CASCADE,
        null=True, blank=True,
    )
