from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from todo_project import settings

User = get_user_model()


def send_email(request, user):
    current_site = get_current_site(request)
    context = {
        "user": user,
        "domain": current_site.domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": token_generator.make_token(user),
    }
    message = render_to_string(
        'accounts/activate.html',
        context=context,
    )
    email = EmailMultiAlternatives(
        subject='Активуйте аккаунт',
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email]
    )
    email.attach_alternative(message, "text/html")
    email.send()
