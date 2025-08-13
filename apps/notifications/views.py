from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import NotificationLog
from .serializers import NotificationLogSerializer
from .tasks import send_notification_task


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = NotificationLog.objects.all()
    serializer_class = NotificationLogSerializer

    def perform_create(self, serializer):
        notification = serializer.save()
        send_notification_task.delay(notification.id)