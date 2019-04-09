"""urbanpiper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from delivery.views import (CurUserTaskView, DvrCurrentTaskView,
                            ModCurrentTaskView, ModifyTaskView,
                            PreviousTaskView, TaskActivityView, TaskHtmlView,
                            UpdateTaskView)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^raise_task/$', TaskHtmlView.as_view(), name='raise_task'),
    url(r'^get_tasks/$', TaskActivityView.as_view(), name='get_tasks'),
    url(r'^modify_task/(?P<task_uuid>[0-9a-z-]+)/$',
        ModifyTaskView.as_view(), name='modify_task'),
    url(r'^update_task/(?P<task_uuid>[0-9a-z-]+)/$',
        ModifyTaskView.as_view(), name='update_task'),
    url(r'^get_cur_task/$', DvrCurrentTaskView.as_view(), name='get_cur_task'),
    url(r'^view_task/(?P<task_uuid>[0-9a-z-]+)/$',
        ModCurrentTaskView.as_view(), name='view_task'),
    url(r'^edit_task/(?P<task_uuid>[0-9a-z-]+)/$',
        ModCurrentTaskView.as_view(), name='edit_task'),
    url(r'^previous_task/$', PreviousTaskView.as_view(), name='previous_task'),
    url(r'^cur_user_task/$', CurUserTaskView.as_view(), name='cur_user_task'),
    url(r'^update_dvr_task/(?P<task_act_uuid>[0-9a-z-]+)/$',
        UpdateTaskView.as_view(), name='update_dvr_task'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'},
        name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logged_out.html'},
        name='logout'),
]
