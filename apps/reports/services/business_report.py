from apps.businesses.models import Business
from apps.appointments.models import Appointment


def get_business_report_data(filters):
    qs = Business.objects.all()

    if filters:
        name = filters.get('name')
        if name:
            qs = qs.filter(name__icontains=name)

    data = []
    for biz in qs:
        total_services = biz.services.count()
        total_appointments = Appointment.objects.filter(service__business=biz).count()

        data.append({
            "id": biz.id,
            "business_name": biz.name,
            "owner": str(biz.owner),
            "total_services": total_services,
            "total_appointments": total_appointments,
            "created_at": biz.created_at.strftime("%Y-%m-%d"),
        })

    return data