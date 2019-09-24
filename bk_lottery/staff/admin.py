# -*- coding: utf-8 -*-

from django.contrib import admin
from staff.models import Staff, StaffList


# Register your models here.


class StaffListAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class StaffAdmin(admin.ModelAdmin):
    list_display = ['name', 'chineseName', 'staffList', 'remark', 'avatar']
    list_filter = ['staffList', ]
    search_fields = ['name']


admin.site.register(StaffList, StaffListAdmin)
admin.site.register(Staff, StaffAdmin)
