from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework.views import APIView

from delivery.constants import (DELIVERY_ALL_TASK, DELIVERY_SELF_TASK,
                                DELIVERY_UPDATE, DELIVERY_VIEW_TASK,
                                MANAGER_ALL_TASK, MANAGER_POST_TASK,
                                MANAGER_VIEW_TASK, NO_TASK, OTHER_LOGGEDIN)
from delivery.dbapi import TaskActivityDbio
from delivery.handlers.dvr_task import DeliveryPerson
from delivery.handlers.mgr_task import ManagerTask
from usermodule.choices import UserType


class TaskActivityView(APIView):

    def get(self, request):
        """
        get all created task
        """
        objs = ManagerTask().get_all_tasks()
        if isinstance(objs, dict):
            return render(request, NO_TASK)

        return render(request, MANAGER_ALL_TASK, {'task_info': objs})


class TaskHtmlView(APIView):
    def get(self, request):
        return render(request, MANAGER_POST_TASK)

    def post(self, request):
        """
        create a new task
        """
        data = request.data
        tkt_obj = None
        if not data.get('title').strip() and (
                not data.get('content').strip()
                ):
            messages.warning(request, 'Please give some input')
        else:
            tkt_obj = ManagerTask().create_task(request, data)
            messages.success(request, 'The Task has been Created')
        return render(request, MANAGER_POST_TASK, {'task_info': tkt_obj})


class ModifyTaskView(APIView):

    def get(self, request, task_uuid):
        task_obj, task_act = ManagerTask().retreive_single_task(task_uuid)
        context = {
            'info': task_obj, 'task_act': task_act
        }
        return render(request, MANAGER_VIEW_TASK, context)

    def post(self, request, task_uuid):
        data = request.data
        if data.get('_method') == 'PUT':
            return self.put(request, task_uuid)
        return self.delete(request, task_uuid)

    def put(self, request, task_uuid):
        data = request.data
        ManagerTask().modify(task_uuid, data)
        messages.success(request, 'The Task has been Updated')
        arg_num = reverse('get_tasks')
        return HttpResponseRedirect(arg_num)

    def delete(self, request, task_uuid):
        ManagerTask().delete_task(task_uuid)
        arg_num = reverse('get_tasks')
        messages.success(request, 'The Task has been Deleted')
        return HttpResponseRedirect(arg_num)


class DvrCurrentTaskView(APIView):

    def get(self, request):
        """
        view task priority wise
        """
        objs = DeliveryPerson().get_by_priority()
        if isinstance(objs, dict):
            return render(request, NO_TASK)

        return render(request, DELIVERY_ALL_TASK, {'info': objs})


class ModCurrentTaskView(APIView):
    def get(self, request, task_uuid):
        """
        view task before accept/reject
        """
        obj, _ = ManagerTask().retreive_single_task(task_uuid)
        return render(request, DELIVERY_VIEW_TASK, {'info': obj})

    def post(self, request, task_uuid):
        """
        update task after accept/reject
        """
        data = request.data
        if data.get('_method') == 'ACCEPT':
            obj = DeliveryPerson().handle_task(request, task_uuid, accept=True)
            if isinstance(obj, dict):
                return self.check_over_limit(obj, request)
            messages.success(request, 'The Task has been Accepted')
            arg_num = reverse('cur_user_task')
            return HttpResponseRedirect(arg_num)
        obj = DeliveryPerson().handle_task(request, task_uuid, accept=False)
        if isinstance(obj, dict):
            return self.check_over_limit(obj, request)
        messages.info(request, 'The Task has been Declined')
        arg_num = reverse('get_cur_task')
        return HttpResponseRedirect(arg_num)

    def check_over_limit(self, obj, request):
        messages.warning(request, obj['message'])
        arg_num = reverse('get_cur_task')
        return HttpResponseRedirect(arg_num)


class PreviousTaskView(APIView):
    def get(self, request):
        """
        view any previous task that has been accepted by the current
        logged-in person
        """
        obj = DeliveryPerson().accepted_by_other(request)
        return render(request, OTHER_LOGGEDIN, {'task_info': obj})


class UpdateTaskView(APIView):
    def get(self, request, task_act_uuid):
        """
        view a previously task before complete/decline
        """
        obj = TaskActivityDbio().get_taskactivity(task_act_uuid)
        return render(request, DELIVERY_UPDATE, {'info': obj})

    def post(self, request, task_act_uuid):
        """
        change task state to complete/decline
        """
        data = request.data
        obj = DeliveryPerson().update_task(request, task_act_uuid, data)
        return render(request, DELIVERY_SELF_TASK, {'task_info': obj})


class CurUserTaskView(APIView):
    def get(self, request):
        if request.user.profile.user_type == UserType.MANAGER:
            arg_num = reverse('get_tasks')
            return HttpResponseRedirect(arg_num)
        """
        view all previously task
        """
        obj = DeliveryPerson().cur_user_tasks(request)
        return render(request, DELIVERY_SELF_TASK, {'task_info': obj})
