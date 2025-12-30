
from django.core.mail import send_mail
from django.conf import settings
import secrets
import string
import pytz
from datetime import datetime

def send_verification_code(user):
    if user is not None:
        digits = string.digits  
        otp = ''.join(secrets.choice(digits) for _ in range(6))
        user.otp_code=otp
        user.otp_created=datetime.now(pytz.utc)
        user.save()
        send_mail(
            subject="Lobace Food account Verification code",
            message=f"Your OTP for email verification is: {otp}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return True
    return False
