from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, FormView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet

from task.forms import AddTaskFormView
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


class CustomTaskApiView(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['completed', 'priority']
    search_fields = ['title']

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)
        return query_set

    def perform_create(self, serializer):
        serializer.save(**{'user': self.request.user})

    @action(methods=['post'], detail=True)
    def mark_as_important(self, request, pk=None):
        task = self.get_object()
        task.importance = True
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def set_status_as_finished(self, request, pk=None):
        task = self.get_object()
        task.set_status_finished()
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def set_status_as_todo(self, request, pk=None):
        task = self.get_object()
        task.set_status_todo()
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def set_status_as_in_progress(self, request, pk=None):
        task = self.get_object()
        task.set_status_in_progress()
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def set_status_as_blocked(self, request, pk=None):
        task = self.get_object()
        task.set_status_blocked()
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def set_priority_as_low(self, request, pk=None):
        task = self.get_object()
        task.priority = 'low'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def set_priority_as_medium(self, request, pk=None):
        task = self.get_object()
        task.priority = 'medium'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def set_priority_as_high(self, request, pk=None):
        task = self.get_object()
        task.priority = 'high'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

