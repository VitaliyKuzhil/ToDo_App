from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

User = get_user_model()


class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             null=True, blank=True, related_name='task')
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline_date = models.DateField()
    COMPLETED_CHOICES = [('todo', 'Потрібно виконати'),
                         ('in_progress', 'В процесі'),
                         ('blocked', 'Заблоковано'),
                         ('finished', 'Виконано')]
    completed = models.CharField(max_length=17, choices=COMPLETED_CHOICES, default='todo')
    PRIORITY_CHOICES = [('low', 'Низький'),
                        ('medium', 'Середній'),
                        ('high', 'Високий')]
    priority = models.CharField(max_length=8, choices=PRIORITY_CHOICES, default='medium')
    importance = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'user: {self.user}'

    def get_absolute_url(self):
        return reverse('task:task_detail', kwargs={'pk': self.pk})
