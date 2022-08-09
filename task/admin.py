from django.contrib import admin
from task.models import Task


class TaskAdmin(admin.ModelAdmin):
    def short_text(self, obj):
        return obj.description[:50]

    list_display = ('title', 'short_text', 'user',)
    search_fields = ('title',)
    list_filter = ('user', 'status', 'priority')
    fields = ('title', 'description', 'user', 'status', 'priority', 'importance',
              'created_date', 'updated_date', 'started_at', 'finished_at')
    readonly_fields = ('user', 'status', 'priority', 'importance',
                       'created_date', 'updated_date', 'started_at', 'finished_at')


admin.site.register(Task, TaskAdmin)
