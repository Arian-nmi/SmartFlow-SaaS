from io import BytesIO
from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from apps.reports.models import Report


def export_report_to_pdf(report, data):
    """Creating a simple PDF based on input data"""

    try:
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)

        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, 800, f"Appointments Report - {report.id}")

        y = 770
        for row in data:
            line = ", ".join(f"{k}: {v}" for k, v in row.items())
            p.drawString(100, y, line)
            y -= 20

        p.save()
        pdf_content = buffer.getvalue()
        buffer.close()

        filename = f"report_{report.id}.pdf"
        report.file_path.save(filename, ContentFile(pdf_content))
        report.status = Report.STATUS_READY
        report.save()
        print(f"[DEBUG] Report {report.id} saved at {report.file_path}")
        return True
    except Exception as e:
        report.status = Report.STATUS_FAILED
        report.save()
        print(f"[ERROR] Report {report.id} PDF generation failed: {e}")
        return False