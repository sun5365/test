# -*- coding: utf-8 -*-

import random
from os import path

import xlrd
from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import HttpResponseBadRequest, JsonResponse

from common.log import logger
from common.mymako import render_mako_context
from lottery.models import Award
from staff.models import Staff, StaffList
from lottery.models import ExclusionForAll




def get_all_staff(request, awardID):
    """
    获取所有中奖者名单
    """
    result = True
    message = ''
    try:
        award = Award.objects.get(id=awardID)
    except Award.DoesNotExist as e:
        logger.error('ERROR: Can\'t get staff by award (%s)' % e)
        message = u'无法获得奖项对应名单中的staff'
        staffs = []
        result = False

    if result:
        staffs = list(Staff.objects.filter(staffList=award.staffList).values('name', 'avatar'))
        random.shuffle(staffs)

    return JsonResponse({
        'staffs': staffs,
        'message': message,
        'result': result
    })


def get_all_staff_as_js(request, awardID):
    """
    给前端返回rtxs数组
    """
    try:
        award = Award.objects.get(id=awardID)
        staffs = list(Staff.objects.filter(staffList=award.staffList)) + list(
            Staff.objects.filter(staffList=award.staffList2))

        random.shuffle(staffs)
    except Award.DoesNotExist as e:
        logger.error("ERROR: Can't get staff by award (%s)" % e)
        staffs = []
    return render_mako_context(request, '/makojs/rtx.js', {
        'rtxs': staffs,
    })


def save_staff_from_excel(request):
    """
    导入中奖者名单
    """

    def escape_html(unsafe):
        # 转换不安全的字符
        return unsafe.replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;").replace('"', "&quot;").replace(
            "'", "&#039;")

    excelFile = request.FILES.get('excel', None)
    staff_png_url = settings.CEPH_STATIC_URL

    if not excelFile:
        return JsonResponse({
            'result': False,
            'message': u"上传名单错误，文件不存在",
        })

    if StaffList.objects.filter(name=excelFile.name).exists():
        return JsonResponse({
            'result': False,
            'message': u'文件（名单）名已经存在，请更改文件名再上传'
        })

    staffs = []
    try:
        staffList = StaffList.objects.create(name=excelFile.name)
        excel = xlrd.open_workbook(file_contents=excelFile.read())
        sheet = excel.sheet_by_index(0)
        # 去掉excel表表头
        tmp_name_list = []  # 去重
        for row in xrange(1, sheet.nrows):
            staff = escape_html(sheet.cell_value(row, 0))
            chinese_name = escape_html(sheet.cell_value(row, 1))
            department = escape_html(sheet.cell_value(row, 2))
            try:
                is_absent = escape_html(sheet.cell_value(row, 3)) == u'报备'
            except IndexError as e:
                is_absent = False
            remark = ''
            if Staff.objects.filter(name=staff).count() == 0 and staff not in tmp_name_list:
                # 数据去重
                candidate = Staff(
                    name=staff,
                    chineseName=chinese_name,
                    remark=remark,
                    department=department,
                    is_absent=is_absent,
                    staffList=staffList,
                )
                avatar_path = path.join("avatars", "{}_small.png".format(staff))
                if finders.find(avatar_path):
                    candidate.avatar = path.join(staff_png_url, "avatars/{}_small.png".format(staff))
                else:
                    candidate.avatar = path.join(staff_png_url, "avatars/default.png")
                staffs.append(candidate)
                tmp_name_list.append(staff)
    except Exception as e:
        StaffList.objects.filter(name=excelFile.name).delete()
        logger.error(u'读取excel文件出错 (%s)' % e)
        return JsonResponse({
            'result': False,
            'message': u"读取excel文件出错:excel文件格式不正确",
        })

    try:
        Staff.objects.bulk_create(staffs)
        result = True
    except Exception as e:
        result = False
        StaffList.objects.filter(name=excelFile.name).delete()
        logger.error(u'批量插入staff数据失败 (%s)' % e)
        message = u'插入数据库失败'

    if result:
        # 报备的人直接放入到大奖排出名单
        absent_staffs = []
        for staff in Staff.objects.filter(is_absent=True):
            absent_staffs.append(ExclusionForAll(staff=staff))

        ExclusionForAll.objects.bulk_create(absent_staffs)

    return JsonResponse({
        'result': result,
        'message': message,
    })


def remove_staff_by_staff_list(request):
    """
    删除指定名单中的人员
    """
    file_name = request.POST.get('fileNames', None)
    if not file_name:
        return HttpResponseBadRequest(u'参数fileNames不存在')
    try:
        staff_list = StaffList.objects.filter(name=file_name)[0]
        Staff.objects.filter(staffList=staff_list).delete()
        staff_list.delete()
    except StaffList.DoesNotExist as e:
        logger.error(u'删除名单失败，请确认已经删除引用该名单的奖项')
        return HttpResponseBadRequest(u'删除名单失败，请确认已经删除引用该名单的奖项')

    return JsonResponse({
        'result': True,
        'message': u'删除成功',
    })


def check_staff_list_can_remove(request):
    """
    检测当前名单是否可以删除
    """
    file_name = request.POST.get('fileNames', None)
    if not file_name:
        return JsonResponse({
            'result': False,
            'message': u'参数file不存在',
        })

    try:
        staff_list = StaffList.objects.get(name=file_name)
    except StaffList.DoesNotExist as e:
        return JsonResponse({
            'result': False,
            'message': u"要删除的名单不存在",
        })

    message = ''
    result = True
    if Award.objects.filter(staffList=staff_list).exists():
        result = False
        message = u'还有奖项引用了该名单'

    return JsonResponse({
        'result': result,
        'message': message,
    })
