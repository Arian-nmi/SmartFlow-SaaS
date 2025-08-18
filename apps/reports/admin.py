from django.contrib import admin
from .models import Report


class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'report_type', 'requested_by', 'status', 'created_at')
    list_filter = ('report_type', 'status')
    search_fields = ('requested_by__username',)

admin.site.register(Report, ReportAdmin)