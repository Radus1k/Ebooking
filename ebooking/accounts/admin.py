from .models import Profile
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin
from .models import Profile

class HotelAdministratorGroupAdmin(GroupAdmin):
    pass

admin.site.unregister(Group)

@admin.register(Group)
class GroupAdmin(HotelAdministratorGroupAdmin):
    pass

def create_hotel_administrator_group(modeladmin, request, queryset):
    group_name = 'Hotel Administrators'
    group, created = Group.objects.get_or_create(name=group_name)
    profiles = Profile.objects.filter(is_hotel_administrator=True)
    for profile in profiles:
        user = profile.user
        user.groups.add(group)
    modeladmin.message_user(request, f'The {group_name} group has been created and users have been added to it.')

create_hotel_administrator_group.short_description = 'Create hotel administrator group'

admin.site.register(Profile)
admin.site.add_action(create_hotel_administrator_group)
