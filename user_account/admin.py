from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from user_account.models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from django.contrib.sessions.models import Session
from django.urls import path, include
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.http import FileResponse
import csv
from events.models import Event_User

# admin.site.register(Profile)
admin.site.register(License)


@admin.register(Event_User)
class Event_UserAdmin(ImportExportModelAdmin):
    pass


# admin.site.register(Code)
# admin.site.register(User_Code)
@admin.register(Session)
class SessionAdmin(ImportExportModelAdmin):
    order_by = ['expire_date']
    list_display = ['session_key', 'expire_date']


class LoggedInUserAdmin(ImportExportModelAdmin):
    readonly_fields = ('created_at',)
admin.site.register(LoggedInUser,LoggedInUserAdmin)


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class UserAdmin(BaseAdmin, ImportExportModelAdmin):
    resource_class = UserResource


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin):
    list_display = ['user', 'state', ]
    search_fields = ('state',)


# @admin.register(Code)
# class CodeAdmin(ImportExportModelAdmin):
#     list_display = ['code']
#     search_fields = ('code',)
#
#
# @admin.register(User_Code)
# class UserCodeAdmin(ImportExportModelAdmin):
#     search_fields = ('user__username', 'code__code',)
