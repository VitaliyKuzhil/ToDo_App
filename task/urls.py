from django.urls import path

from task.views import TaskListView, ProfileView, TaskDetailView

urlpatterns = [
    path('', TaskListView.as_view(), name='list_task'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('profile/', ProfileView.as_view(), name='user_profile')
]
