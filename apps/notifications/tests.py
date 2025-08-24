from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.notifications.models import NotificationLog


User = get_user_model()

class NotificationLogModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@test.com", password="12345")

    def test_create_notification_default_status(self):
        """Notification should be created with status=pending by default"""
        notif = NotificationLog.objects.create(
            recipient=self.user,
            notification_type=NotificationLog.TYPE_EMAIL,
            title="Welcome",
            message="Hello and welcome!"
        )
        self.assertEqual(notif.status, NotificationLog.STATUS_PENDING)

    def test_notification_str(self):
        notif = NotificationLog.objects.create(
            recipient=self.user,
            notification_type=NotificationLog.TYPE_SMS,
            title="Test SMS",
            message="Hello!"
        )
        expected = f"sms to {self.user} - pending"
        self.assertEqual(str(notif), expected)

    def test_notification_can_change_status_to_sent(self):
        notif = NotificationLog.objects.create(
            recipient=self.user,
            notification_type=NotificationLog.TYPE_EMAIL,
            title="Reminder",
            message="Meeting at 10am"
        )
        notif.status = NotificationLog.STATUS_SENT
        notif.save()
        self.assertEqual(notif.status, NotificationLog.STATUS_SENT)

    def test_notification_related_to_user(self):
        notif = NotificationLog.objects.create(
            recipient=self.user,
            notification_type=NotificationLog.TYPE_EMAIL,
            message="Test relation"
        )
        self.assertEqual(notif.recipient, self.user)
        self.assertEqual(self.user.notifications.first(), notif)