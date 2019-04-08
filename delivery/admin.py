from django.contrib import admin

from delivery.models import Task, TaskActivity


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_by', 'priority', 'state',)
    search_fields = ('title', 'content', 'created_by', 'priority', 'state',)


@admin.register(TaskActivity)
class TaskActivityAdmin(admin.ModelAdmin):
    list_display = ('task', 'deliver_man', 'state', 'time')

    def deliver_man(self, obj):
        return obj.dvr_man

    def time(self, obj):
        return obj.created_at

    search_fields = ('task', 'accepted_by', 'state',)
    readonly_fields = ['created_by', 'modified_by']
