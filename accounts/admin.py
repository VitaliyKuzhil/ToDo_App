from datetime import datetime, timedelta
from django.utils import timezone

from django.contrib import admin

from django.template.response import TemplateResponse
from django.urls import path

from accounts.models import CustomUser
from task.models import Task
from task.constants import TaskStatusChoices, TaskPriorityChoices

from django.contrib.auth import get_user_model
from rest_framework.authtoken.admin import TokenAdmin

User = get_user_model()
TokenAdmin.raw_id_fields = ['user']


class TaskInline(admin.TabularInline):
    model = Task
    can_delete = False
    verbose_name_plural = 'task'

    def short_text(self, obj):
        return obj.description[:50]

    fields = ('title', 'short_text')
    readonly_fields = ('title', 'short_text')
    extra = 0


class UserAdmin(admin.ModelAdmin):
    change_list_template = "user_change_list.html"

    def get_urls(self):
        urls = [
            path("dashboard/", self.admin_site.admin_view(self.info_dashboard_view),
                 name='dashboard', ),
        ] + super(UserAdmin, self).get_urls()
        return urls

    def info_dashboard_view(self, request):
        tasks = Task.objects.all()
        user = User.objects.all()

        context = {
            **self.admin_site.each_context(request),
            'user_count': user.count(),
            'auth_user_last_week': user.filter(date_joined__gt=datetime.now(timezone.utc) - timedelta(days=7)).count(),
            'all_task': tasks.count(),
            'status_todo': tasks.filter(status=TaskStatusChoices.TODO).count(),
            'status_in_progress': tasks.filter(status=TaskStatusChoices.IN_PROGRESS).count(),
            'status_blocked': tasks.filter(status=TaskStatusChoices.BLOCKED).count(),
            'status_finished': tasks.filter(status=TaskStatusChoices.FINISHED).count(),
            'priority_high': tasks.filter(priority=TaskPriorityChoices.HIGH).count(),
            'priority_medium': tasks.filter(priority=TaskPriorityChoices.MEDIUM).count(),
            'priority_low': tasks.filter(priority=TaskPriorityChoices.LOW).count(),
        }
        return TemplateResponse(request, "info_dashboard.html", context)

    def task_count(self, obj):
        return obj.task.count()

    task_count.short_description = 'Tasks count'

    list_display = ('id', 'first_name', 'last_name', 'position', 'email', 'task_count')
    list_display_links = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name')
    inlines = [TaskInline]

    fields = (('first_name', 'last_name'), 'email', 'blocked')
    fieldsets = None
    add_fieldsets = (
        (
            None,
            {
                "classes": ('wide',),
                "fields": ('first_name', 'last_name', 'email', "password1", "password2"),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['first_name', 'last_name', 'email']
        return []


inlines = [TaskInline]
admin.site.register(CustomUser, UserAdmin)
