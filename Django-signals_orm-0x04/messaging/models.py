from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

from messaging.views import UnreadMessagesManager


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    password = models.CharField(max_length=128, null=True, blank=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField("First Name", max_length=255)
    last_name = models.CharField("Last Name", max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True)


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_reciver')
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_editor', null=True)
    edited_at = models.DateTimeField(null=True)
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True)
    read = models.BooleanField(default=False)

    objects = models.Manager()
    unread = UnreadMessagesManager()



class Notification(models.Model):
    notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class MessageHistory(models.Model):
    history_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='message_history')
    