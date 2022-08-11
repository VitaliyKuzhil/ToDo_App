from datetime import date, timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives, send_mass_mail
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


@app.task
def send_email_every_morning_celery():
    messages = []
    for user in User.objects.all():
        subject = 'Щоденні нагадування дедлайнів'
        message = f'Hey, {user.first_name}.'
        tasks = user.task.filter(deadline_date=date.today() + timedelta(days=1))
        if tasks.count():
            message += ' Завтра дедлайн таких завдань:\n'
            for task in tasks:
                message += f'\t{task.title}\n'

        messages.append((subject, message, settings.EMAIL_HOST_USER, [user.email]))
    send_mass_mail(datatuple=tuple(messages))


@app.task
def send_email_every_week_celery():
    messages = []
    for user in User.objects.all():
        subject = 'Ваші виконані завдання цього тижня'
        message = f'Hey, {user.first_name}.'
        end_date = timezone.now()
        start_date = end_date - timedelta(days=7)
        tasks = user.task.filter(finished_at__range=[start_date, end_date])
        if tasks.count():
            message += ' Виконані завдання цього тижня:\n'
            for task in tasks:
                message += f'\t{task.title}\n'

        messages.append((subject, message, settings.EMAIL_HOST_USER, [user.email]))

    send_mass_mail(datatuple=tuple(messages))
