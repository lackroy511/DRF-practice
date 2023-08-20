from django.core.management import BaseCommand
from course.tasks import check_last_login_date

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):

        # user = User.objects.create(
        #     email='1',
        #     is_staff=True,
        #     is_superuser=True,
        #     is_active=True,
        # )
        
        # user = User.objects.filter(email='1').first()

        # user.is_active = True
        # user.set_password('1')
        # user.save()
        
        check_last_login_date()
        
