from celery import shared_task
from .models import Report
from .services.appointment_report import get_appointment_report_data
from .exporters.pdf_exporter import export_report_to_pdf
from .exporters.excel_exporter import export_report_to_excel
from apps.notifications.models import NotificationLog
import logging


logger = logging.getLogger(__name__)

@shared_task
def generate_report_task(report_id):
    try:
        report = Report.objects.get(id=report_id)
        logger.warning(f"[CELERY] Generating report ID={report.id}, type={report.report_type}")

        if report.report_type == Report.TYPE_APPOINTMENTS:
            data = get_appointment_report_data(report.filters)
        else:
            data = []

        output_format = (report.filters or {}).get('format', 'pdf')
        if output_format == 'excel':
            export_report_to_excel(report, data)
        else:
            export_report_to_pdf(report, data)

        report.status = Report.STATUS_READY
        report.save()

        NotificationLog.objects.create(
            recipient=report.requested_by,
            notification_type=NotificationLog.TYPE_EMAIL,
            title="Your report is ready",
            message=f"Report {report.id} has been generated and is ready for download."
        )

        logger.warning(f"[CELERY] Data size: {len(data)} rows")
    except Exception as e:
        report.status = Report.STATUS_FAILED
        report.save()
        logger.error(f"[CELERY][ERROR] Report {report_id} failed: {str(e)}")