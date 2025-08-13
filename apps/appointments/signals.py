from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from apps.notifications.models import NotificationLog


@receiver(post_save, sender=settings.APPOINTMENT_MODEL)
def send_appointment_notification(sender, instance, created, **kwargs):
    if created:
        NotificationLog.objects.create(
            recipient=instance.user,
            notification_type=NotificationLog.TYPE_EMAIL,
            title="Your appointment is booked",
            message=f"Dear {instance.user.first_name}, your appointment with {instance.business.name} is booked for {instance.date}."
        )