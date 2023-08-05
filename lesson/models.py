from django.db import models

from course.models import Course


class Lesson(models.Model):

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    name = models.CharField(
        max_length=150, verbose_name='Название курса',
    )
    description = models.TextField(
        verbose_name='Описание курса',
    )
    image = models.ImageField(
        upload_to='course_img_preview', null=True, blank=True, verbose_name='Изображение курса',
    )
    video_url = models.URLField(
        max_length=250, verbose_name='url на видео', null=True, blank=True,
    )
    course = models.ForeignKey(
        Course, verbose_name='Курс', on_delete=models.CASCADE,
        null=True, blank=True, related_name='course',
    )

    def __str__(self):
        return f'Урок: {self.name}'
