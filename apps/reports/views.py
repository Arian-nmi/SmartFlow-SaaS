from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Report
from .serializers import ReportSerializer
from .tasks import generate_report_task


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        report = serializer.save()
        generate_report_task.delay(report.id)