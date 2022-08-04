from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, FormView

from task.forms import AddTaskFormView
from task.models import Task


class TaskListView(View):
    paginate_by = 5

    def get(self, request: HttpRequest):
        list_todo = Task.objects.all().filter(user=self.request.user).order_by('-id')
        context = {'list_todo': list_todo}
        return render(request, 'task/list_task.html', context=context)


class TaskDetailView(View):
    def get(self, request: HttpRequest, pk):
        task = get_object_or_404(Task, pk=pk, user=self.request.user)
        context = {"task": task}
        return render(request, 'task/task_detail.html', context)


class UpdateTaskView(UpdateView):
    model = Task
    fields = ['title', 'description', 'deadline_date', 'completed', 'priority', 'importance']
    template_name = 'task/update_task_detail.html'
    template_name_suffix = '_update_task_detail'


class AddTaskView(FormView):
    form_class = AddTaskFormView
    success_url = reverse_lazy("task:list_task")
    template_name = "task/add_task.html"

    def form_valid(self, form):
        task = form.save(commit=False)
        task.user = self.request.user
        task.save()
        return super().form_valid(form)


class StatisticTask(View):
    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        finished_task = tasks.exclude(success_data__isnull=True)
        statistics_bool = False

        try:
            time = sum([(task.success_data - task.created_date).seconds for task in finished_task])
            average_duration_task = time // finished_task.count()
        except ZeroDivisionError:
            average_duration_task = 0
            statistics_bool = True

        context = {
            'all_task': tasks.count(),
            'status_todo': tasks.filter(status='todo').count(),
            'status_in_progress': tasks.filter(status='in_progress').count(),
            'status_blocked': tasks.filter(status='blocked').count(),
            'status_finished': tasks.filter(status='finished').count(),
            'average_duration_task':
                f'{average_duration_task // 3600} hours '
                f'{(average_duration_task // 60) % 60} minutes',
            'statistic': statistics_bool,
        }
        return render(request, 'task/staistic.html', context=context)
