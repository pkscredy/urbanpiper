from django.db import models

from base.models import AbstractAuditModel
from delivery.choices import (
            PriorityStatus,
            StatesStatus,
            PRIORITY_CHOICES,
            STATE_STATUS_CHOICES
        )
from usermodule.models import Profile


class Task(AbstractAuditModel):
    title = models.CharField(max_length=200, blank=True, null=True)
    content = models.CharField(max_length=2000, blank=True, null=True)
    created_by = models.ForeignKey(Profile, related_name='profile',
                                   blank=True, null=True,
                                   on_delete=models.CASCADE)
    priority = models.IntegerField(
                                default=PriorityStatus.STATUS_NOT_SET,
                                choices=PRIORITY_CHOICES
                        )
    state = models.IntegerField(
                                default=StatesStatus.NEW,
                                choices=STATE_STATUS_CHOICES
                        )

    def __str__(self):
        return '%s ' % (self.title)


class TaskActivity(AbstractAuditModel):
    task = models.ForeignKey(Task, related_name='task',
                             blank=True, null=True,
                             on_delete=models.CASCADE)
    dvr_man = models.ForeignKey(Profile, related_name='dvr_man',
                                blank=True, null=True,
                                on_delete=models.CASCADE)
    state = models.IntegerField(
                                default=StatesStatus.NEW,
                                choices=STATE_STATUS_CHOICES
                        )
