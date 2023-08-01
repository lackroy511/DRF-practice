# Generated by Django 4.2.3 on 2023-08-01 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название курса')),
                ('description', models.TextField(verbose_name='Описание курса')),
                ('image', models.ImageField(blank=True, null=True, upload_to='course_img_preview', verbose_name='Изображение курса')),
                ('video_url', models.URLField(max_length=250, verbose_name='url на видео')),
            ],
            options={
                'verbose_name': 'Урок',
                'verbose_name_plural': 'Уроки',
            },
        ),
    ]
