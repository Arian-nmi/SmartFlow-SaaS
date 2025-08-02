from django.urls import path
from .views import SendOTPView, VerifyOTPView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
