from django.contrib.auth.models import User
from django.db import models

from base.models import AbstractAuditModel
from usermodule.choices import (GENDER_CHOICES, USERTYPE_CHOICES, Gender,
                                UserType)


class Profile(AbstractAuditModel):
    user = models.OneToOneField(User, related_name='profile',
                                on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=10, blank=True, null=True,
                                     db_index=True)
    country_code = models.CharField(max_length=2, default='91')
    first_name = models.CharField(('first name'), max_length=30, blank=True,
                                  null=True)
    last_name = models.CharField(('last name'), max_length=30, blank=True,
                                 null=True)
    email = models.EmailField(('email address'), unique=True, null=True,
                              blank=True)
    pan_no = models.CharField(max_length=200, blank=True, null=True)
    aadhaar_no = models.CharField(max_length=200, blank=True, null=True)
    local_address = models.CharField(max_length=500, null=True, blank=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.IntegerField(
                            default=Gender.STATUS_NOT_SET,
                            choices=GENDER_CHOICES
                        )
    user_type = models.IntegerField(
                                default=UserType.STATUS_NOT_SET,
                                choices=USERTYPE_CHOICES
                        )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'Profiles'

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return '{}'.format(self.first_name)
