from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import smtplib
from email.mime.text import MIMEText


def send_mail(to, template, context):
    html_content = render_to_string(f'accounts/emails/{template}.html', context)
    text_content = render_to_string(f'accounts/emails/{template}.txt', context)
    msg = EmailMultiAlternatives(context['subject'], text_content, settings.DEFAULT_FROM_EMAIL, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


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

        # server.login('username', 'password')
        server.sendmail(sender, receivers, context)

        print("**** Mail sent...*****")

    send_mail(email, 'restore_password_email', context)