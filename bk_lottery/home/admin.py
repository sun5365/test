from django.contrib import admin

# Register your models here.

from home.models import AppMetaConfig


@admin.register(AppMetaConfig)
class AppConfigAdmin(admin.ModelAdmin):
    list_display = ['conf_name', 'conf_value', 'remark']