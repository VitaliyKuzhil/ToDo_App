from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from .constants import TaskStatusChoices, TaskPriorityChoices

User = get_user_model()


class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             null=True, blank=True, related_name='task')
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline_date = models.DateField()

    status = models.CharField(max_length=16, choices=TaskStatusChoices.choices, default=TaskStatusChoices.TODO)
    priority = models.CharField(max_length=8, choices=TaskPriorityChoices.choices, default=TaskPriorityChoices.MEDIUM)

    importance = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    started_at = models.DateTimeField(null=True, default=None)
    finished_at = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return f'user: {self.user}'

    def get_absolute_url(self):
        return reverse('task:task_detail', kwargs={'pk': self.pk})

    def set_status_as_in_progress(self):
        self.status = TaskStatusChoices.IN_PROGRESS
        self.started_at = timezone.now()

    def set_status_as_finished(self):
        self.status = TaskStatusChoices.FINISHED
        self.finished_at = timezone.now()
