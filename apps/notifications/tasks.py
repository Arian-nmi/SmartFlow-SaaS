from celery import shared_task
from .services import process_notification


@shared_task
def send_notification_task(notification_id):
    process_notification(notification_id)