from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline_date = models.DateField()
    completed = models.CharField(max_length=20)
    priority = models.CharField(max_length=20)
    importance = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"user: {self.user}, title: {self.title}, importance {self.importance}" \
               f" priority: {self.priority}, completed: {self.completed}, deadline: {self.deadline_date}"

