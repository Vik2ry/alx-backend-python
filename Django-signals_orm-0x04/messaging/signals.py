from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.db.models.signals import post_save, pre_save, post_delete

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(message=instance, user=instance.receiver)


@receiver(pre_save, sender=Message)
def create_message_history(sender, instance, **kwargs):
    if instance.pk and Message.objects.get(pk=instance.pk):
        MessageHistory.objects.create(message=instance)


@receiver(post_delete, sender=MessageHistory)
def clear_user_data(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(sender=instance).delete()
