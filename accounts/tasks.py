from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as token_generator

from todo_project import settings
from todo_project.celery import app

User = get_user_model()


@app.task
def send_email_celery(user_id, site_domain):
    user = User.objects.get(id=user_id)

    context = {
        "user": user,
        "domain": site_domain,
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
    return email.send()
