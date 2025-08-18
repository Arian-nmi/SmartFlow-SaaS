from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Report(models.Model):
    """The main model for managing reports"""

    TYPE_APPOINTMENTS = 'appointments'
    TYPE_BUSINESSES = 'businesses'
    TYPE_CHOICES = [
        (TYPE_APPOINTMENTS, 'Appointments'),
        (TYPE_BUSINESSES, 'Businesses')
    ]

    STATUS_PENDING = 'pending'
    STATUS_READY = 'ready'
    STATUS_FAILED = 'failed'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_READY, 'Ready'),
        (STATUS_FAILED, 'Failed'),
    ]

    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    filters = models.JSONField(blank=True, null=True)
    file_path = models.FileField(upload_to='reports/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.report_type} ({self.status})"

    class Meta:
        ordering = ['-created_at']