# -*- coding: utf-8 -*-
from PIL import Image
from cStringIO import StringIO
from django.contrib import admin, messages
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponseRedirect
from lottery.models import Plan, Award, Winner, Exclusion, WheelItem, ExclusionForAll
from django.conf import settings

import base64


# Register your models here.

def make_thumb(file, default_width=300):
    """
    生成缩略图/压缩图
    """
    pixbuf = Image.open(file)
    width, height = pixbuf.size

    # 如果宽度大于default_width，则进行压缩
    if width > default_width:
        delta = width / default_width
        height = int(height / delta)
        pixbuf.thumbnail((default_width, height), Image.ANTIALIAS)

    temp_file = StringIO()
    pixbuf.save(temp_file, pixbuf.format)
    return temp_file


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'status']
    exclude = ['status']
    actions = ['make_activated', 'make_inactivated']

    def make_activated(self, request, queryset):
        count = Plan.objects.filter(status=1).count()
        if queryset.count() > 1 or count >= 1:
            self.message_user(request, u'只允许一个方案为激活状态', level=messages.ERROR)
        else:
            queryset.update(status=1)

    make_activated.short_description = u'更新为激活状态'

    def make_inactivated(self, request, queryset):
        queryset.update(status=0)
        count = queryset.count()
        self.message_user(request, u'%d条记录更新为未激活状态' % count, level=messages.SUCCESS)

    make_inactivated.short_description = u'更新为未激活状态'


def my_clean(self):
    from django import forms
    form_data = self.cleaned_data
    if form_data['number'] != form_data['winRate'] + form_data['winRate2']:
        raise forms.ValidationError(u"输入的中奖人数不符合要求！请重新填写！")
    # if form_data['staffList'] == form_data['staffList2']:
    #     raise forms.ValidationError(u"不能选择两个相同的名单！")
    return form_data


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ['name', 'prize', 'times', 'number', 'status', 'plan',
                    'everyoneCanDraw', 'takeInScene', 'changeWinRateInPlace', 'isAddToExclusion']
    exclude = ['image']
    actions = ['make_activated', 'make_all_acticated']
    fieldsets = (
        (None, {'fields': ('name', 'prize', 'picture', 'status', 'plan')}),
        ('设置', {'fields': ('sequence', 'needInput', 'everyoneCanDraw', 'takeInScene',
                           'changeWinRateInPlace', 'isAddToExclusion')}),
        (None, {'fields': ('number', 'staffList', 'winRate', 'staffList2', 'winRate2'),
                'description': '<span style="color:red">*每次中奖人数要等于名单1和名单2中奖人数之和</span>'})
    )

    def save_form(self, request, form, change):
        """
        Given a ModelForm return an unsaved instance. ``change`` is True if
        the object is being changed, and False if it's being added.
        """
        new_object = form.save(commit=False)
        file = request.FILES.get('picture', None)
        if file:
            new_object.compressed_picture = InMemoryUploadedFile(make_thumb(new_object.picture.file), None,
                                                                 new_object.picture.name, None, 0, None)
        new_object.save()
        return new_object

    def make_activated(self, request, queryset):
        count = Award.objects.filter(status=1).count()
        if queryset.count() > 1 or count >= 1:
            self.message_user(request, u'只允许一个奖项为激活状态', level=messages.ERROR)
        else:
            queryset.update(status=1)

    make_activated.short_description = u'更新为激活状态'

    def make_all_acticated(self, request, queryset):
        awards = Award.objects.all()
        awards.update(status=1)

    make_all_acticated.short_description = u'激活全部奖项'

    def make_inactivated(self, request, queryset):
        queryset.update(status=0)
        count = queryset.count()
        self.message_user(request, u'%d条记录更新为未激活状态' % count, level=messages.SUCCESS)

    make_inactivated.short_description = u'更新为未激活状态'

    def response_change(self, request, obj, post_url_continue=None):
        next = request.GET.get('next', None)
        if next is not None:
            return HttpResponseRedirect(settings.SITE_URL)
        else:
            return super(AwardAdmin, self).response_change(request, obj)

    def response_add(self, request, obj, post_url_continue=None):
        next = request.GET.get('next', None)
        if next is not None:
            return HttpResponseRedirect(settings.SITE_URL)
        else:
            return super(AwardAdmin, self).response_change(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        form = admin.ModelAdmin.get_form(self, request, obj, **kwargs)
        form.clean = my_clean
        return form

    def save_model(self, request, obj, form, change):
        file = request.FILES.get('picture', None)
        if file:
            compressed_file_string = base64.b64encode(obj.compressed_picture.file.read())
            encodedString = base64.b64encode(obj.picture.file.read())
            obj.image = 'data:image/jpg;base64,' + encodedString
            obj.compressed_image = 'data:image/jpg;base64,' + compressed_file_string
            obj.save()
        else:
            obj.save()


@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ['staff', 'award', 'remark']
    actions = ['delete_all']

    def delete_all(self, request, queryset):
        Winner.objects.all().delete()

    delete_all.short_description = u'删除全部'


@admin.register(Exclusion)
class ExclusionAdmin(admin.ModelAdmin):
    list_display = ['staff', 'award']


# @admin.register(WheelItem)
class WheelItemAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(ExclusionForAll)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ['staff']
    actions = ['delete_all']

    def delete_all(self, request, queryset):
        ExclusionForAll.objects.all().delete()

    delete_all.short_description = u'删除全部'