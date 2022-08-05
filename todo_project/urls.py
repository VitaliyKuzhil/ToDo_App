"""todo_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts.views import CustomAuthToken
from accounts.urls import user_router
from task.urls import task_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('task/', include('task.urls', namespace="task"), name='task'),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token/', CustomAuthToken.as_view(), name='token_generator'),
    path('user-api/', include(user_router.urls), name='user_router'),
    path('task-api/', include(task_router.urls), name='task_router'),
]
