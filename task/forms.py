import datetime
from django import forms
from task.models import Task
from task.constants import TaskStatusChoices, TaskPriorityChoices


class AddTaskFormView(forms.ModelForm):
    title = forms.CharField(max_length=200,
                            label='Назва завдання',
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Опис завдання',
                                  widget=forms.Textarea(attrs={'class': 'form-control', "rows": 3}))
    deadline_date = forms.DateField(label='Дата дедлайну',
                                    initial=datetime.date.today,
                                    widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline_date']


class UpdateTaskFormView(forms.ModelForm):
    title = forms.CharField(max_length=200,
                            label='Назва завдання',
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Опис завдання',
                                  widget=forms.Textarea(attrs={'class': 'form-control', "rows": 3}))
    deadline_date = forms.DateField(label='Дата дедлайну',
                                    initial=datetime.date.today,
                                    widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    status = forms.ChoiceField(label='Статус виконання',
                               choices=TaskStatusChoices.choices,
                               widget=forms.Select(attrs={'class': 'form-control'}))
    priority = forms.ChoiceField(label='Пріорітет',
                                 choices=TaskPriorityChoices.choices,
                                 widget=forms.Select(attrs={'class': 'form-control'}))

    importance = forms.BooleanField(label='Важливість',
                                    required=False)

    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline_date', 'status', 'priority', 'importance']
