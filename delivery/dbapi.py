from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone

from base.dbapi import AbstractBaseDbIO
from delivery.models import Task, TaskActivity


class TaskDbio(AbstractBaseDbIO):

    @property
    def model(self):
        return Task

    def get_task(self, task_uuid):
        return TaskDbio().get_object(
            {
                'uuid': task_uuid
            }
        )

    def update_task_state(self, obj, state):
        return TaskDbio().update_obj(
            obj, {'state': state}
        )

    def filter_by_priority(self, priority, state):
        return TaskDbio().filter_objects(
            {
                'priority': priority,
                'state': state
            }
        ).last()


class TaskActivityDbio(AbstractBaseDbIO):

    @property
    def model(self):
        return TaskActivity

    def get_taskactivity(self, task_uuid):
        return TaskActivityDbio().get_object(
            {
                'uuid': task_uuid
            }
        )

    def various_state(self, task_uuid):
        return TaskActivity.objects.select_related('task').filter(
            task__uuid=task_uuid
        ).order_by('created_at')

    @staticmethod
    def get_current_users():
        active_sessions = Session.objects.filter(
            expire_date__gte=timezone.now()
        )
        user_id_list = []
        for session in active_sessions:
            data = session.get_decoded()
            user_id_list.append(data.get('_auth_user_id', None))
        # Query all logged in users based on id list
        return User.objects.filter(id__in=user_id_list)
