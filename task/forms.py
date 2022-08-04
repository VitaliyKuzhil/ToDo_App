import datetime
from django import forms
from django.utils.translation import gettext_lazy as _
from task.models import Task


class AddTaskFormView(forms.ModelForm):
    title = forms.CharField(max_length=200,
                            label='Назва завдання',
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Опис завдання',
                                  widget=forms.Textarea(attrs={'class': 'form-control', "rows": 3}))
    deadline_date = forms.DateField(label='Дата дедлайну',
                                    initial=datetime.date.today,
                                    widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    COMPLETED_CHOICES = [('todo', 'Потрібно виконати'),
                         ('in_progress', 'В процесі'),
                         ('blocked', 'Заблоковано'),
                         ('finished', 'Виконано')]
    completed = forms.ChoiceField(label='Статус виконання',
                                  choices=COMPLETED_CHOICES,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    PRIORITY_CHOICES = [('high', 'Низький'),
                        ('medium', 'Середній'),
                        ('low', 'Високий')]
    priority = forms.ChoiceField(label='Пріорітет',
                                 choices=PRIORITY_CHOICES,
                                 widget=forms.Select(attrs={'class': 'form-control'}))

    importance = forms.BooleanField(label='Важливість',
                                    required=False)

    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline_date', 'completed', 'priority', 'importance']
