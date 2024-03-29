from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from .models import Reservation


def send_mail(to, template, context):
    html_content = render_to_string(f'emails/{template}', context)
    text_content = render_to_string(f'emails/{template}', context)
    msg = EmailMultiAlternatives(context['subject'], text_content, settings.DEFAULT_FROM_EMAIL, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

def send_reservation_mail(to, reservation):
    #!/usr/bin/python

    import smtplib
    from email.mime.text import MIMEText

    sender = 'order@ebooking.local'
    receivers = ['test@mailhog.local'] # some user who enters his email

    body_msg = "You have reserved rooms with success"
    # hotel name -> reservation.hotelroom.hotel.name
    header = "Dear " + reservation.first_name + reservation.last_name + "\n Thanks for reservation \n here are your reservation data: "
    body = "Check in : " + str(reservation.begin_at) + "\n" + "Check out: " + str(reservation.ends_at) + "\n" + "Observations: " + reservation.observations + "\n\n" + "Enjoy!!" 

    port = 1025
    msg = MIMEText(header + body)

    msg['Subject'] = 'Ebooking order'
    msg['From'] = sender
    msg['To'] = to
    
    print("Sending mail...")

    with smtplib.SMTP('host.docker.internal', port) as server:

        # server.login('username', 'password')
        server.sendmail(sender, receivers, msg.as_string())

        print("**** Mail sent...*****")