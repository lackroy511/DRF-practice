
from django.db import models

# Create your models here.


class Course(models.Model):

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    name = models.CharField(
        max_length=150, verbose_name='название курса',
    )
    description = models.TextField(
        verbose_name='Описание курса',
    )
    image = models.ImageField(
        upload_to='course_img_preview', null=True, blank=True, verbose_name='изображение курса',
    )
    video_url = models.URLField(
        max_length=250, verbose_name='url на видео', null=True, blank=True,
    )
    owner = models.ForeignKey(
        'users.User', verbose_name='владелец',
        on_delete=models.CASCADE, blank=True, null=True,
    )

    def __str__(self):
        return f'Курс: {self.name}'


class Lesson(models.Model):

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    name = models.CharField(
        max_length=150, verbose_name='название курса',
    )
    description = models.TextField(
        verbose_name='описание курса',
    )
    image = models.ImageField(
        upload_to='course_img_preview', null=True, blank=True, verbose_name='изображение курса',
    )
    video_url = models.URLField(
        max_length=250, verbose_name='url на видео', null=True, blank=True,
    )
    course = models.ForeignKey(
        Course, verbose_name='Курс', on_delete=models.CASCADE,
        null=True, blank=True, related_name='lessons',
    )
    owner = models.ForeignKey(
        'users.User', verbose_name='владелец',
        on_delete=models.CASCADE, null=True, blank=True,
    )

    def __str__(self):
        return f'Урок: {self.name}'
