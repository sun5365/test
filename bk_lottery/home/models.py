# -*- coding: utf-8 -*-


from django.db import models

# Create your models here.

from django.db import  models


class AppMetaConfig(models.Model):
    """
    APP相关配置
    """
    conf_name = models.CharField(u'配置名称', max_length=64)
    conf_value = models.TextField(u'配置值')
    remark = models.CharField(u'备注', max_length=128, default='无')

    def __unicode__(self):
        return u'APP配置'

    class Meta:
        verbose_name = '配置表'
        verbose_name_plural = u'配置表'