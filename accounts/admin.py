from django.contrib import admin
from django.contrib.auth import get_user_model

from accounts.models import CustomUser
from task.models import Task

User = get_user_model()


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

    def task_count(self, obj):
        return obj.task.count()

    list_display = ('first_name', 'last_name', 'position', 'email', 'task_count')
    list_display_links = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name')
    inlines = [TaskInline]

    fields = (('first_name', 'last_name'), 'email', 'task_count')
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
            obj.tasks_count = obj.task.count()
            return ['first_name', 'last_name', 'email', 'task_count']
        else:
            return []


inlines = [TaskInline]
admin.site.register(CustomUser, UserAdmin)
