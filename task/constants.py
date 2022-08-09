from django.db import models


class TaskStatusChoices(models.TextChoices):
    TODO = 'todo', 'Потрібно виконати'
    IN_PROGRESS = 'in_progress', 'В процесі'
    BLOCKED = 'blocked', 'Заблоковано'
    FINISHED = 'finished', 'Виконано'


class TaskPriorityChoices(models.TextChoices):
    LOW = 'low', 'Низький'
    MEDIUM = 'medium', 'Середній'
    HIGH = 'high', 'Високий'
