from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Avg, F
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, FormView, DeleteView, CreateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, request
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet

from task.constants import TaskPriorityChoices, TaskStatusChoices
from task.forms import AddTaskFormView, UpdateTaskFormView
from task.models import Task
from task.serializers import TaskSerializer

User = get_user_model()


class TaskListView(View):

    def get(self, request: HttpRequest):
        list_todo = Task.objects.all().filter(user=self.request.user).order_by('-id')
        paginator = Paginator(list_todo, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        if request.method == 'GET' and 'search' in request.GET:
            search = request.GET['search']
            page_obj = Task.objects.filter(title__icontains=search).order_by('-id')

        context = {'page_obj': page_obj}
        return render(request, 'task/list_task.html', context=context)


class TaskDetailView(View):
    def get(self, request: HttpRequest, pk):
        task = get_object_or_404(Task, pk=pk, user=self.request.user)
        context = {"task": task}
        return render(request, 'task/task_detail.html', context)


class UpdateTaskView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = UpdateTaskFormView
    template_name = 'task/update_task_detail.html'
    template_name_suffix = '_update_task_detail'

    def form_valid(self, form):
        task = form.save(commit=False)
        if task.status == TaskStatusChoices.IN_PROGRESS:
            task.set_status_as_in_progress()
        elif task.status == TaskStatusChoices.FINISHED:
            task.set_status_as_finished()
        task.save()
        return super(UpdateTaskView, self).form_valid(form)


class AddTaskView(LoginRequiredMixin, CreateView):
    form_class = AddTaskFormView
    success_url = reverse_lazy("task:list_task")
    template_name = "task/add_task.html"

    def form_valid(self, form):
        task = form.save(commit=False)
        task.user = self.request.user
        task.save()
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('task:list_task')


class StatisticTask(View):
    def get(self, request: HttpRequest):
        tasks = Task.objects.filter(user=self.request.user)

        context = {
            'all_task': tasks.count(),
            'status_todo': tasks.filter(status='todo').count(),
            'status_in_progress': tasks.filter(status='in_progress').count(),
            'status_blocked': tasks.filter(status='blocked').count(),
            'status_finished': tasks.filter(status='finished').count(),
            'priority_high': tasks.filter(priority='high').count(),
            'priority_medium': tasks.filter(priority='medium').count(),
            'priority_low': tasks.filter(priority='low').count(),
            **tasks.filter(status='finished').aggregate(avg_resolution_time=Avg(F('finished_at') - F('started_at')))
        }
        return render(request, 'task/statistic.html', context=context)


class CustomTaskApiView(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'priority']
    search_fields = ['title']

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)
        return query_set

    def perform_create(self, serializer):
        serializer.save(**{'user': self.request.user})

    @action(methods=['post'], detail=True)
    def task_importance(self, request, pk=None):
        task = self.get_object()
        task.importance = True
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def set_status_todo(self, request, pk=None):
        task = self.get_object()
        task.status = TaskStatusChoices.TODO
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def set_status_in_progress(self, request, pk=None):
        task = self.get_object()
        task.status = TaskStatusChoices.IN_PROGRESS
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def set_status_blocked(self, request, pk=None):
        task = self.get_object()
        task.status = TaskStatusChoices.BLOCKED
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def set_status_finished(self, request, pk=None):
        task = self.get_object()
        task.status = TaskStatusChoices.FINISHED
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def set_priority_low(self, request, pk=None):
        task = self.get_object()
        task.priority = TaskPriorityChoices.LOW
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def set_priority_medium(self, request, pk=None):
        task = self.get_object()
        task.priority = TaskPriorityChoices.MEDIUM
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def set_priority_high(self, request, pk=None):
        task = self.get_object()
        task.priority = TaskPriorityChoices.HIGH
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

