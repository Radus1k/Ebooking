from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import smtplib
from email.mime.text import MIMEText
from celery import shared_task
from reservation.mail import send_mail

@shared_task
def send_reset_password_email(request, email, token, uid):
    sender = 'accounts@ebooking.local'
    receivers = ['test@mailhog.local'] # some user who enters his email

    context = {
        'subject': _('[Managemnt Hotelier] - Resetare parolă'),
        'uri': request.build_absolute_uri(
            reverse('accounts:restore_password_confirm', kwargs={'uidb64': uid, 'token': token})),
    }

    port = 1025
    
    print("Sending reset password mail...")

    with smtplib.SMTP('host.docker.internal', port) as server:
        try:
            server.sendmail(sender, receivers, str(context))
        except smtplib.SMTPException as e:
            print(f"An error occurred: {e}")
        except Exception as e:
            print("error", e)
        else:
            print("**** Mail sent...*****")

    send_mail(email, 'restore_password_email.html', context)