from celery import shared_task
import time


@shared_task
def send_otp_sms(phone_number, otp):
    time.sleep(2)
    print(f"OTP for {phone_number}: {otp}")
    return True
