from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def send_email(email):
    email.send()


def send_verification_email(request, user, token):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    mail_subject = 'Activate your account'
    current_site = str(get_current_site(request))
    activation_uri = 'http://{}{}?uid={}&token={}'.format(current_site,
                                                           reverse('user:verification'),
                                                           uid,
                                                           token.key
                                                           )

    message = render_to_string('user/email_verification.html', {
        'user': user,
        'activation_uri': activation_uri
    })

    email = EmailMessage(
        mail_subject, message, to=[user.email], from_email=settings.EMAIL_HOST_USER
    )

    email.content_subtype = 'html'
    send_email(email)

    return email
