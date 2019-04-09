from delivery.choices import PriorityStatus, StatesStatus
from delivery.constants import MAX_LIMIT
from delivery.dbapi import TaskActivityDbio, TaskDbio
from usermodule.choices import UserType


class DeliveryPerson:
    def get_by_priority(self):
        state = StatesStatus.NEW
        high_obj = TaskDbio().filter_by_priority(PriorityStatus.HIGH, state)
        if high_obj:
            return high_obj
        med_obj = TaskDbio().filter_by_priority(PriorityStatus.MEDIUM, state)
        if med_obj:
            return med_obj
        low_obj = TaskDbio().filter_by_priority(PriorityStatus.LOW, state)
        if low_obj:
            return low_obj
        return {
            'message': 'No Task are available'
        }

    def handle_task(self, request, task_uuid, accept):
        if request.user.profile.dvr_man.filter(
                state=StatesStatus.ACCEPTED).count() == MAX_LIMIT:
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
