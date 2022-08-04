from django.contrib import admin
from task.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user',)
    search_fields = ('title',)
    list_filter = ('user__first_name',)
    fields = ('title', 'description', 'user', 'completed')
    readonly_fields = ('user',)


admin.site.register(Task, TaskAdmin)
