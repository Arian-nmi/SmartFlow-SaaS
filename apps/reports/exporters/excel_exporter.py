from io import BytesIO
from django.core.files.base import ContentFile
from openpyxl import Workbook


def export_report_to_excel(report, data):
    """Creating simple Excel from data"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Report"

    if data:
        ws.append(list(data[0].keys()))
    for row in data:
        ws.append(list(row.values()))

    buffer = BytesIO()
    wb.save(buffer)

    excel_content = buffer.getvalue()
    buffer.close()

    report.file_path.save(f"report_{report.id}.xlsx", ContentFile(excel_content))
    return report