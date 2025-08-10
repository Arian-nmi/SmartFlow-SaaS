from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.accounts.urls')),
    path('api/businesses/', include('apps.businesses.urls')),
    path('api/appointments/', include('apps.appointments.urls')),
]
