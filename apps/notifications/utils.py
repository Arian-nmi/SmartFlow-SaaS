from django.core.mail import send_mail


def send_email(recipient_email, subject, body):
    """Sending simple emails using Django's default SMTP"""

    return send_mail(
        subject,
        body,
        'no-reply@smartflow.com',
        [recipient_email],
        fail_silently=False
    )

def send_sms(phone_number, body):
    """Send SMS (currently a mock - in practice it must connect to the service provider's API)"""

    print(f"SMS to {phone_number}: {body}")
    return True