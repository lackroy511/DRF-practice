from celery import shared_task
from django.core.mail import send_mail

from datetime import date
from users.models import User


@shared_task
def send_course_update_email(emails: list) -> None:
    
    send_mail(
        subject='Материалы курса обновлены',
        message='test',
        from_email='djang5111@gmail.com',
        recipient_list=emails,
    )


@shared_task
def check_last_login_date() -> None:
    
    users = User.objects.all()
    
    for user in users:
        
        if user.last_login:
            date_diff = date.today() - user.last_login
                
            if date_diff and date_diff.days >= 30:
                user.is_active = False
                user.save()
