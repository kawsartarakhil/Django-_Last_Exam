from django.core.mail import send_mail
from django.conf import settings
def custom_send_email_confirmation(token):
    send_mail(
        subject="Please Confirm your email",
        message=f"Click on this link to login : http://127.0.0.1:8000/confirm/{token.token}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[token.user.email]
    )

def send_reset_password_email(token):
    send_mail(
        subject="Reset your password",
        message=f"Click this link to reset your password: http://127.0.0.1:8000/reset-password/{token.token}/",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[token.user.email]
    )
