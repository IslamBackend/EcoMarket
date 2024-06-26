import random
import string

from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

code = random.randint(1000, 9999)


def send_confirmation_email(user):
    subject = _('Email Confirmation')
    message = (
        f"Hello! Your email address was provided for logging into the EcoMarket application. "
        f"Please enter this code on the login page: {code}. "
        f"If this was not you, please ignore this email."
    )
    email_from = settings.EMAIL_HOST_USER

    try:
        send_mail(subject, message, email_from, [user.email], fail_silently=False)
    except Exception as e:
        print(f"Error sending confirmation email: {e}")

    user.otp = code
    user.save()


def send_password_reset_email(email, reset_password):
    subject = _("Password Reset")
    message = _(
        f"Password reset code: {reset_password}. The code is valid for 5 minutes."
    )
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])


def generate_random_code(length=4):
    characters = string.digits
    return "".join(random.choice(characters) for _ in range(length))
