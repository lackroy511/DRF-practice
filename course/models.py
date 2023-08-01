from django.db import models

# Create your models here.


class Course(models.Model):

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    name = models.CharField(max_length=150, verbose_name='Название курса')
    description = models.TextField(verbose_name='Описание курса')
    image = models.ImageField(upload_to='course_img_preview', null=True,
                              blank=True, verbose_name='Изображение курса')
