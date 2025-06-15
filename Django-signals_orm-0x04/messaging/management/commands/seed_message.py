from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from messaging.models import Message

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User = get_user_model()

        user = User.objects.first()
        Message.objects.create(receiver=user, sender=user, content='dslkjflasdjflsadjlfsaj')
