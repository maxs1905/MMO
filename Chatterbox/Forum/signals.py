from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Response

@receiver(post_save, sender=Response)
def notify_new_response(sender, instance, created, **kwargs):
    if created:
        instance.send_notification()

@receiver(post_save, sender=Response)
def notify_accepted_response(sender, instance, **kwargs):
    if instance.is_accepted and not kwargs.get('created'):
        instance.send_accept_notification()