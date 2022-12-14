# Generated by Django 4.0.6 on 2022-08-13 20:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('deadline_date', models.DateField()),
                ('status', models.CharField(choices=[('todo', 'Потрібно виконати'), ('in_progress', 'В процесі'), ('blocked', 'Заблоковано'), ('finished', 'Виконано')], default='todo', max_length=16)),
                ('priority', models.CharField(choices=[('low', 'Низький'), ('medium', 'Середній'), ('high', 'Високий')], default='medium', max_length=8)),
                ('importance', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('started_at', models.DateTimeField(default=None, null=True)),
                ('finished_at', models.DateTimeField(default=None, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
