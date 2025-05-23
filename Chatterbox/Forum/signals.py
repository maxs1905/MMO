from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Response

@receiver(post_save, sender=Response)
def send_response_notification(sender, instance, created, **kwargs):
    if created:
        instance.send_notification()
    elif instance.is_accepted:
        instance.send_accept_notification()