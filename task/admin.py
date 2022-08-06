from django.contrib import admin
from task.models import Task


class TaskAdmin(admin.ModelAdmin):
    def short_text(self, obj):
        return obj.description[:50]

    list_display = ('title', 'short_text', 'user',)
    search_fields = ('title',)
    list_filter = ('user', 'completed', 'priority')
    fields = ('title', 'description', 'user', 'completed')
    readonly_fields = ('user',)


admin.site.register(Task, TaskAdmin)
