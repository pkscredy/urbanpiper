from delivery.dbapi import TaskActivityDbio, TaskDbio
from delivery.models import Task


class ManagerTask:
    def create_task(self, request, data):
        task_data = {
            'title': data.get('title'),
            'content': data.get('content'),
            'priority': data.get('priority'),
            'created_by': request.user.profile
        }
        return TaskDbio().create_obj(task_data)

    def get_all_tasks(self):
        objs = Task.objects.all().order_by('state')
        if not objs:
            return {
                'message': 'No Task are available'
            }
        return objs

    def retreive_single_task(self, task_uuid):
        return (
                TaskDbio().get_task(task_uuid),
                TaskActivityDbio().various_state(task_uuid)
            )

    def modify(self, task_uuid, data):
        obj = TaskDbio().get_object(
            {
                'uuid': task_uuid
            }
        )
        tkt_data = {
            'title': data.get('title', obj.title),
            'content': data.get('content', obj.content),
            'priority': data.get('priority', obj.priority),
            'state': data.get('state', obj.state)
        }
        return TaskDbio().update_obj(obj, tkt_data)

    def delete_task(self, task_uuid):
        TaskDbio().get_object(
            {
                'uuid': task_uuid
            }
        ).delete()
        return {
            'message': 'task deleted'
        }
