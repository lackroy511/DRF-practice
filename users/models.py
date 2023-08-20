from django.contrib.auth.models import AbstractUser
from django.db import models

from course.models import Course, Lesson

# Create your models here.


class User(AbstractUser):

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    username = None
    email = models.EmailField(
        unique=True, verbose_name='почта',
    )
    last_login = models.DateField(
        auto_now=False, auto_now_add=False, verbose_name='дата последнего входа',
        null=True, blank=True,
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
    amount = models.PositiveIntegerField(
        verbose_name='Сумма платежа',
    )
    stripe_payment_id = models.CharField(
        max_length=255, verbose_name='id платежа stripe',
        null=True, blank=True,
    )
    status = models.CharField(
        max_length=10, verbose_name='статус платежа', default='open',
        )
    stripe_payment_url = models.TextField(
        verbose_name='id платежа stripe', null=True, blank=True,
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
    

class Subscription(models.Model):

    class Meta:
        verbose_name = 'подписка на курс'
        verbose_name_plural = 'подписки на курс'

    course_name = models.CharField(
        max_length=255, verbose_name='название курса', null=True, blank=True,
    )
    course = models.ForeignKey(
        'course.Course', verbose_name='курс', on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    user = models.ForeignKey(
        'users.User', verbose_name='пользователь', on_delete=models.CASCADE,
        related_name='subscriptions',
    )

    def __str__(self):
        return f'{self.course} {self.user}'

    def save(self, *args, **kwargs):
        self.course_name = self.course.name

        return super(Subscription, self).save(*args, **kwargs)
