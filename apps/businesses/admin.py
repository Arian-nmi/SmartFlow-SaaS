from django.contrib import admin
from .models import Business


class BusinessAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'phone', 'created_at')
    search_fields = ('name', 'owner__email')

admin.site.register(Business, BusinessAdmin)