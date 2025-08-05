from django.contrib import admin
from .models import Service, Appointment


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'business', 'price', 'duration', 'capacity')
    search_fields = ('name', 'business__name')


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'service', 'user', 'date', 'time', 'status')
    search_fields = ('service__name', 'user__email')
    list_filter = ('status', 'date')

admin.site.register(Service, ServiceAdmin)
admin.site.register(Appointment, AppointmentAdmin)