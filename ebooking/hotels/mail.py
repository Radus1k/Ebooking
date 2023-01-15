from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _


def send_mail(to, template, context):
    html_content = render_to_string(f'emails/{template}', context)
    text_content = render_to_string(f'emails/{template}', context)
    msg = EmailMultiAlternatives(context['subject'], text_content, settings.DEFAULT_FROM_EMAIL, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

def send_mail_v2(to, hotelRooms):
    #!/usr/bin/python

    import smtplib
    from email.mime.text import MIMEText

    sender = 'test@mailhog.local'
    receivers = ['test@mailhog.local'] # some user who enters his email

    body_msg = "You have reserved rooms with success"

    port = 1025
    msg = MIMEText('Thank you for the reservation')

    msg['Subject'] = 'Ebooking order'
    msg['From'] = sender
    msg['To'] = to
    
    print("Sending mail...")

    with smtplib.SMTP('host.docker.internal', port) as server:

        # server.login('username', 'password')
        server.sendmail(sender, receivers, msg.as_string())

        print("**** Mail sent...*****")