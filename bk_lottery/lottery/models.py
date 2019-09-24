# -*- coding: utf-8 -*-

from django.db import models

from staff.models import Staff, StaffList


# Create your models here.

class Plan(models.Model):
    """
    抽奖计划/方案表
    说明：每个奖项都属于一个特定的抽奖计划/方案，处于未激活状态抽奖计划下的所有奖项都不可以抽奖
    """
    name = models.CharField(u'抽奖计划名称', max_length=64)
    description = models.CharField(u'抽奖计划描述', max_length=1024)
    status = models.IntegerField(u'状态', default=0, choices=(
        (0, u'未激活'),
        (1, u'已激活'),
    ))

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = u'抽奖计划'
        verbose_name_plural = u'抽奖计划'


class Award(models.Model):
    """
    奖项表
    说明：设置奖项的必要信息(中奖总人数，中奖者名单，所属中奖计划等)，还可设置以下开关
        1. 是否需要短信进行通知: 给中奖者发送短信
        2. 是否现场输入奖品: 奖品名称可以现场输入，为了方便重抽，抽奖页面有再抽一次按钮
        3. 是否所有人都可以抽奖: 如果打开该设置，则该奖项中奖候选人将包含之前已中过奖的人员，否则则不包括
        4. 是否现场领奖: 如果打开该设置，则对于每个中奖人员都可以实现重抽(当中奖人缺席)
        5. 是否可以现场更改人数
        6. 中奖人员是否添加到排除名单(设置了所有人抽奖的也不能中奖)
    """
    name = models.CharField(u'奖项名称', max_length=64)
    number = models.IntegerField(u'每次中奖人数', default=1)
    staffList = models.ForeignKey(StaffList, verbose_name=u'关联名单1', on_delete=models.PROTECT, related_name="staff_list")
    winRate = models.IntegerField(u'名单1中奖人数', default=0)
    staffList2 = models.ForeignKey(StaffList, verbose_name=u'关联名单2', on_delete=models.PROTECT,
                                   related_name="staff_list_2",
                                   null=True)
    winRate2 = models.IntegerField(u'名单2中奖人数', default=0)

    times = models.IntegerField(u'抽奖次数', default=1)
    prize = models.CharField(u'奖品', max_length=64)
    plan = models.ForeignKey(Plan, verbose_name=u'抽奖计划')
    status = models.IntegerField(u'状态', default=1, choices=(
        (0, u'未激活'),
        (1, u'已激活'),
        (2, u'已结束'),
    ))
    sequence = models.IntegerField(u'顺序', default=0)
    picture = models.ImageField(u'奖品图片', upload_to='award')
    compressed_picture = models.ImageField(u'压缩图片', upload_to='compressed_award', null=True, blank=True)
    compressed_image = models.TextField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    needInput = models.BooleanField(u'是否现场输入奖品', help_text=u"设置为true表示可以不关闭抽奖页面上连续抽奖和修改奖品内容", default=False)
    changeWinRateInPlace = models.BooleanField(u'是否可以现场更改中奖人数', help_text=u"设置为true表示可以临时调整人数进行修改", default=False)

    everyoneCanDraw = models.BooleanField(u'是否所有人都可以抽奖', help_text=u"设置为true表示该奖可以跟其他奖项重复中奖", default=False)
    isAddToExclusion = models.BooleanField(u'中奖人员是否加到排除名单', help_text=u"设置为true，中了该奖的人员，无法再参与重复抽奖", default=False)
    takeInScene = models.BooleanField(u'是否现场领奖', help_text=u"现场领奖需要人在现场，不在现场可以重新抽取", default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'奖项'
        verbose_name_plural = u'奖项'

    def set_finish(self):
        # winners = Winner.objects.filter(award=award)
        # if winners.count() == award.number * award.times:
        self.status = 2
        self.save()


class Winner(models.Model):
    """
    中奖者表
    说明: 每个中奖者属于一个特定的奖项对象和一个人员对象
    """
    staff = models.ForeignKey(Staff, verbose_name=u'中奖者名称')
    award = models.ForeignKey(Award, verbose_name=u'奖项')
    # 对于用到大转盘的奖项，将会记录大转盘的结果
    remark = models.CharField(u'备注', max_length=256, null=True, blank=True)

    def __unicode__(self):
        return u'winner %s for %s' % (self.staff.name, self.award.name)

    class Meta:
        verbose_name = u'中奖人员'
        verbose_name_plural = u'中奖人员'


class Exclusion(models.Model):
    """
    排除名单表
    说明: 每个奖项的中奖者候选名单将排除该名单上的人员
          该表为特定奖项特定的排除人员
    """
    staff = models.ForeignKey(Staff, verbose_name=u'中奖者名称')
    award = models.ForeignKey(Award, verbose_name=u'奖项')

    def __unicode__(self):
        return u'exclusion：%s' % self.staff.name

    class Meta:
        verbose_name = u'排除名单'
        verbose_name_plural = u'排除名单'


class ExclusionForAll(models.Model):
    """
    排除名单
    说明: 所有奖项都排除该名单上的人员，包括设置了所有人中奖选项的奖项
    """
    staff = models.ForeignKey(Staff, verbose_name=u'中奖者名称')

    def __unicode__(self):
        return u'exclusion：%s' % self.staff.name

    class Meta:
        verbose_name = u'排除名单ForAll'
        verbose_name_plural = u'排除名单ForAll'


class WheelItem(models.Model):
    title = models.CharField(u'标题', max_length=16)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'大转盘项'
        verbose_name_plural = u'大转盘项'
