from django.contrib import admin

from usermodule.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'gender',
                    'user_type', 'mobile_number',)

    search_fields = ('uuid', 'first_name', 'mobile_number')
