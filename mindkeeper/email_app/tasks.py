from celery import shared_task
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from society.models import User


@shared_task
def send_email(email_data):
    send_mail(
        subject=email_data['subject'],
        recipient_list=email_data['recipient_list'],
        from_email=settings.EMAIL_HOST_USER,
        message=email_data['message'],
    )


@shared_task
def send_verify_email(user_pk):

    user = get_object_or_404(User, pk=user_pk)
    context = {
        'user': user,
        'domain': '127.0.0.1:8000',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'protocol': 'http'
    }

    message = render_to_string('society/verify_mail.html', context=context)

    send_mail(
        subject='Подтверждение почты',
        recipient_list=[user.email],
        from_email=settings.EMAIL_HOST_USER,
        message=message,

    )
