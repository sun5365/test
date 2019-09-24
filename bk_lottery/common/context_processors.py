# coding=utf-8
'''
context_processor for common(setting)

** 除setting外的其他context_processor内容，均采用组件的方式(string)
'''
from django.conf import settings
from home.models import AppMetaConfig


def mysetting(request):
    try:
        conf = AppMetaConfig.objects.get(conf_name='department')
        department = conf.conf_value
    except AppMetaConfig.DoesNotExist:
        department = u'幸运大抽奖'

    return {
        'MEDIA_URL': settings.MEDIA_URL,  # MEDIA_URL
        'STATIC_URL': settings.STATIC_URL,  # 本地静态文件访问
        'CEPH_STATIC_URL': settings.CEPH_STATIC_URL,
        'STATIC_VERSION': settings.STATIC_VERSION,
        'APP_CODE': settings.APP_CODE,  # 在蓝鲸系统中注册的  "应用编码"
        'APP_PATH': request.get_full_path(),
        'SITE_URL': settings.SITE_URL,  # URL前缀
        'DEPARTMENT': department
    }
