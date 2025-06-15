from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
            User = get_user_model()
            user = User.objects.create_user(
                  username="bin",
                email="bin@gmail.com",
                password="1qaz2wsx",
                first_name='bin',
                last_name='mek',
                phone_number='092525222',
                date_of_birth='1980-05-13' 
        ) 