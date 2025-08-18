from apps.appointments.models import Appointment

def get_appointment_report_data(filters):
    qs = Appointment.objects.all()

    # فیلتر تاریخ
    if filters:
        start = filters.get('date_from')
        end = filters.get('date_to')
        if start:
            qs = qs.filter(date__gte=start)
        if end:
            qs = qs.filter(date__lte=end)

    data = []
    for app in qs:
        data.append({
            "id": app.id,
            "customer": str(app.user),
            "service": str(app.service),
            "business": str(app.service.business),
            "date": app.date.strftime("%Y-%m-%d") if app.date else "",
            "time": app.time.strftime("%H:%M") if app.time else "",
            "status": app.status,
        })

    return data