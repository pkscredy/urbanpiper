from delivery.dbapi import TaskDbio, TaskActivityDbio
from delivery.choices import PriorityStatus, StatesStatus
from usermodule.choices import UserType


class DeliveryPerson:
    def get_by_priority(self):
        # import ipdb; ipdb.set_trace()
        objs = TaskDbio().filter_objects(
            {
                'priority': PriorityStatus.HIGH,
                'state': StatesStatus.NEW
            }
        )
        if objs:
            return objs.last()
        objs = TaskDbio().filter_objects(
            {
                'priority': PriorityStatus.MEDIUM,
                'state': StatesStatus.NEW
            }
        )
        if objs:
            return objs.last()
        objs = TaskDbio().filter_objects(
            {
                'priority': PriorityStatus.LOW,
                'state': StatesStatus.NEW
            }
        )
        if objs:
            return objs.last()
        return {
            'message': 'No Task are available'
        }

    def handle_task(self, request, task_uuid, accept):
        if request.user.profile.dvr_man.filter(
                state=StatesStatus.ACCEPTED).count() == 3:
            return {
                'message': 'You accept limit of task is over'
            }
        obj = TaskDbio().get_task(task_uuid)
        data = {
            'task': obj,
            'dvr_man': request.user.profile
        }
        if accept:
            return self.accept_task(obj, data)
        data['state'] = StatesStatus.DECLINED
        return TaskActivityDbio().create_obj(data)

    def accept_task(self, obj, data):
        data['state'] = StatesStatus.ACCEPTED
        TaskActivityDbio().create_obj(data)
        return TaskDbio().update_obj(
            obj, {'state': StatesStatus.ACCEPTED}
        )

    def accepted_by_other(self, request):
        cur_user = TaskActivityDbio.get_current_users()
        dvr_man = [user.profile for user in cur_user
                   if user.profile.user_type == UserType.DELIVERY]
        return TaskActivityDbio().filter_objects(
            {
                'dvr_man__in': dvr_man,
                'state': StatesStatus.ACCEPTED
            }
        ).exclude(dvr_man=request.user.profile)

    def cur_user_tasks(self, request):
        return TaskActivityDbio().filter_objects(
            {
                'dvr_man': request.user.profile
            }
        )

    def update_task(self, request, task_act_uuid, data):
        obj = TaskActivityDbio().get_taskactivity(task_act_uuid)
        TaskActivityDbio().update_obj(obj, {'state': data.get('state')})
        if obj.state == StatesStatus.COMPLETED:
            TaskDbio().update_task_state(
                obj.task, StatesStatus.COMPLETED
            )
        elif obj.state == StatesStatus.DECLINED:
            TaskDbio().update_task_state(
                obj.task, StatesStatus.NEW
            )
        return self.cur_user_tasks(request)
