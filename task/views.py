from django.shortcuts import render
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import DetailView

from task.models import Task


class TaskListView(View):
    def get(self, request: HttpRequest):
        list_todo = Task.objects.all().filter(user=self.request.user).order_by('-id')
        context = {'list_todo': list_todo}
        return render(request, 'task/list_task.html', context=context)


class TaskDetailView(View):
    def get(self, request: HttpRequest, pk):
        task = get_object_or_404(Task, pk=pk, user=self.request.user)
        context = {"task": task}
        return render(request, 'task/task_detail.html', context)


class ProfileView(View):
    def get(self, request: HttpRequest):
        user = self.request.user
        context = {'user': user}
        return render(request, 'task/user_profile.html', context=context)


