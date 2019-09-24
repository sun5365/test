# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.


class StaffList(models.Model):
    name = models.CharField(u'名单名称', max_length=32, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'名单'
        verbose_name_plural = u'名单'
        ordering = ['id']


class Staff(models.Model):
    name = models.CharField(u'英文名', max_length=16)
    chineseName = models.CharField(u'中文名', max_length=64, blank=True, null=True)
    department = models.CharField(u'部门', max_length=64, blank=True, null=True)
    phone = models.CharField(u'电话', max_length=16, blank=True, null=True)
    avatar = models.CharField(u'头像', max_length=256, blank=True, null=True)
    is_absent = models.BooleanField(u"是否缺席",  default=False)
    remark = models.CharField(u'备注', max_length=256, blank=True, null=True)

    staffList = models.ForeignKey(StaffList, verbose_name=u'名单名称')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Staff'
        verbose_name_plural = u'Staff'
