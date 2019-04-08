# from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
# from rest_framework import status
# from rest_framework.response import Response
from rest_framework.views import APIView

# from ticket.constants import RAISE_TICKET_TEMPLATE, All_TICKET_TEMPLATE
from delivery.dbapi import TaskActivityDbio
from delivery.handlers.mgr_task import ManagerTask
from delivery.handlers.dvr_task import DeliveryPerson


class TaskActivityView(APIView):

    def get(self, request):
        """
        get all created task
        """
        objs = ManagerTask().get_all_tasks()
        if isinstance(objs, dict):
            return render(request, 'no_task.html')

        return render(request, 'all_task.html', {'task_info': objs})


class TaskHtmlView(APIView):
    def get(self, request):
        return render(request, 'post_task.html')

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
        return render(request, 'post_task.html', {'task_info': tkt_obj})


class ModifyTaskView(APIView):

    def get(self, request, task_uuid):
        task_obj, task_act = ManagerTask().retreive_single_task(task_uuid)
        context = {
            'info': task_obj, 'task_act': task_act
        }
        return render(request, 'view_task.html', context)

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
        # return render(request, 'view_task.html', {'info': obj})

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
            return render(request, 'no_task.html')

        return render(request, 'd_all_task.html', {'info': objs})


class ModCurrentTaskView(APIView):
    def get(self, request, task_uuid):
        """
        view task before accept/reject
        """
        obj, _ = ManagerTask().retreive_single_task(task_uuid)
        return render(request, 'd_view_task.html', {'info': obj})

    def post(self, request, task_uuid):
        """
        update task after accept/reject
        """
        data = request.data
        if data.get('_method') == 'ACCEPT':
            obj = DeliveryPerson().handle_task(request, task_uuid, accept=True)
            if isinstance(obj, dict):
                return self.check_over_limit(obj, request)
            return render(request, 'd_view_task.html', {'info': obj})
        obj = DeliveryPerson().handle_task(request, task_uuid, accept=False)
        if isinstance(obj, dict):
            return self.check_over_limit(obj, request)
        return render(request, 'd_view_task.html', {'info': obj})

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
        return render(request, 'd_other_task.html', {'task_info': obj})


class UpdateTaskView(APIView):
    def get(self, request, task_act_uuid):
        """
        view a previously task before complete/decline
        """
        obj = TaskActivityDbio().get_taskactivity(task_act_uuid)
        return render(request, 'd_update_task.html', {'info': obj})

    def post(self, request, task_act_uuid):
        """
        change task state to complete/decline
        """
        data = request.data
        obj = DeliveryPerson().update_task(request, task_act_uuid, data)
        return render(request, 'd_mytask.html', {'task_info': obj})


class CurUserTaskView(APIView):
    def get(self, request):
        """
        view all previously task
        """
        obj = DeliveryPerson().cur_user_tasks(request)
        return render(request, 'd_mytask.html', {'task_info': obj})
