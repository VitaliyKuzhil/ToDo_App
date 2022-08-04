from django.urls import path

from task.views import TaskListView, TaskDetailView, UpdateTaskView, AddTaskView, StatisticTask

app_name = "task"

urlpatterns = [
    path('', TaskListView.as_view(), name='list_task'),
    path('add_task/', AddTaskView.as_view(), name="add_task"),
    path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('update-task-detail/<int:pk>/', UpdateTaskView.as_view(), name='update_task_detail'),
    path('statistic/', StatisticTask.as_view(), name='statistic'),
]
