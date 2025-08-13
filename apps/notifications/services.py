from .utils import send_email, send_sms
from .models import NotificationLog


def process_notification(notification_id):
    """
    A function that reads a specific NotificationLog from the database and sends it based on its type.
    """
    notification = NotificationLog.objects.get(id=notification_id)

    try:
        if notification.notification_type == NotificationLog.TYPE_EMAIL:
            send_email(notification.recipient.email, notification.title, notification.message)
        elif notification.notification_type == NotificationLog.TYPE_SMS:
            send_sms(notification.recipient.phone_number, notification.message)
        notification.status = NotificationLog.STATUS_SENT
    except Exception as e:
        notification.status = NotificationLog.STATUS_FAILED
    notification.save()