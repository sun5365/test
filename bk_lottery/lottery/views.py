# -*- coding: utf-8 -*-
import random
import xlwt
from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404

from common.log import logger
from common.mymako import render_mako_context

from lottery.decorator import execute_time
from lottery.models import Award, Exclusion, Plan, WheelItem, Winner, ExclusionForAll
from lottery.utils import save_winners, xls_to_response
from staff.models import Staff


def get_award_view(request, award_id):
    """
    抽奖首页视图函数
    """
    award = get_object_or_404(Award, id=award_id)
    awards = list(Award.objects.filter(plan=award.plan).order_by('sequence'))
    last_award = None
    next_award = None
    for index, item in enumerate(awards):
        if item.id == int(award_id):
            if index > 0:
                last_award = awards[index - 1]
            if index < len(awards) - 1:
                next_award = awards[index + 1]
            break

    return render_mako_context(request, '/lottery/award.html', {
        'award': award,
        'last_award': last_award,
        'next_award': next_award,
    })


def get_draw_again_view(request):
    """
    再抽一次
    """
    award_id = request.GET['award_id']
    award = get_object_or_404(Award, id=award_id)
    award.status = 1
    award.pk = None  # 以原award记录为原型复制一条新的award记录
    award.save()

    award.save(update_fields=['name'])

    return render_mako_context(request, '/lottery/award.html', {
        'award': award,
        'last_award': None,
        'next_award': None,
    })


def check_status(request):
    """
    返回每个奖项的状态(是否已激活)
    """
    award = Award.objects.all()
    award_status_list = [{'id': item.id, 'name': item.name, 'status': item.status} for item in award]
    return JsonResponse({
        'result': True,
        'message': award_status_list,
    })


def set_award_prize(request, award_id):
    """
    现场输入奖品页面中更新奖项奖品的接口
    """
    prize = request.POST.get('prize', None)
    result = True
    if prize:
        message = ''
        Award.objects.filter(id=award_id).update(prize=prize)
    else:
        message = u'缺少接口必要参数'
        result = False

    return JsonResponse({
        'result': result,
        'message': message,
    })


@execute_time
def select_all_winners_by_award(request, award_id):
    """
    随机选择奖项的所有中奖者
    """
    if settings.DEBUG is False:
        if not request.user.is_superuser:
            return HttpResponseForbidden()

    result = False
    message = ''
    selected = []

    award = get_object_or_404(Award, id=award_id)

    if not (award and award.status != 2):
        # 状态2表示该奖项已结束
        return JsonResponse({
            'winners': selected,
            'result': result,
            'message': u'获取奖项失败或者该奖项已结束',
        })

    try:
        winners = []
        if award.everyoneCanDraw:
            exclusions = [item.staff.name for item in ExclusionForAll.objects.all()]
        else:
            exclusions = [item.staff.name for item in Exclusion.objects.filter(award=award)]
            winners = [item.staff.name for item in Winner.objects.all().exclude(remark__exact='forall')]

        # 中奖候选人去掉排除名单和已经中奖且中奖有效的人员
        staffs = Staff.objects.filter(staffList=award.staffList).exclude(name__in=exclusions). \
            exclude(name__in=winners).values('id', 'name', 'chineseName', 'is_absent')
        staffs2 = Staff.objects.filter(staffList=award.staffList2).exclude(name__in=exclusions). \
            exclude(name__in=winners).values('id', 'name', 'chineseName', 'is_absent')

        try:
            selected = random.sample(staffs, award.winRate)
            selected2 = random.sample(staffs2, award.winRate2)
        except BaseException as error:
            logger.error(u"抽奖无效，当前待抽奖人员不够 %s" % str(error))
            return JsonResponse({
                'winners': [],
                'result': False,
                'message': u"抽奖无效，当前待抽奖人员不够"
            })

        selected.extend(selected2)
        for item in selected:
            if item['is_absent']:
                item['chineseName'] = u"%s(报备)" % item['chineseName']

        # 更新数据库
        save_winners(selected, award)
        award.set_finish()

        if award.isAddToExclusion:
            # 设置的时候不影响当次抽取结果
            try:
                staffs_obj = Staff.objects.filter(name__in=[item['name'] for item in selected])
                poor_guys = [ExclusionForAll(staff=item) for item in staffs_obj]
                ExclusionForAll.objects.bulk_create(poor_guys)
            except BaseException as e:
                logger.error(u"设置排除人员出错 %s" % str(e))

        result = True

    except Staff.DoesNotExist as e:
        logger.error(u'ERROR: can\'t get a winners from staffs (%s)' % e)
        if e.__class__ == ValueError:
            message = u"该奖项获奖人数已超过人员名单剩余人数"
        else:
            message = str(e)

    return JsonResponse({
        'winners': selected,
        'result': result,
        'message': message,
    })


def get_winners_view(request):
    """
    查看当前中奖者页面
    """
    try:
        message = ''
        plan = Plan.objects.get(status=1)
        result = True
    except Plan.DoesNotExist:
        message = u'当前没有激活状态的方案或有多个激活状态的方案'
        result = False
        plan = None
    return render_mako_context(request, '/lottery/winners.html', {
        'plan': plan,
        'message': message,
        'result': result,
    })


def get_all_winners(request):
    """
    获取当前中奖者列表
    用于初始化kendo的Grid
    """

    winners = [{
        'name': winner.staff.name,
        'chineseName': winner.staff.chineseName,
        'department': winner.staff.department,
        'award': winner.award.name,
        'prize': winner.award.prize,
    } for winner in Winner.objects.exclude(remark=u'中奖无效').order_by('award')]

    return JsonResponse(winners, safe=False)


def download_winners_list(request):
    winners = Winner.objects.all().exclude(remark__contains=u"中奖无效")

    wb = xlwt.Workbook()
    ws = wb.add_sheet(u'中奖者名单')

    fields = [u'staff帐号', u'中文名', u'部门', u'奖项', u'奖品名称', u'备注']

    for index, field in enumerate(fields):
        ws.write(0, index, field)

    for index, winner in enumerate(winners):
        ws.write(index + 1, 0, winner.staff.name)
        ws.write(index + 1, 1, winner.staff.chineseName)
        ws.write(index + 1, 2, winner.staff.department)
        ws.write(index + 1, 3, winner.award.name)
        ws.write(index + 1, 4, winner.award.prize)
        ws.write(index + 1, 5, winner.remark)

    return xls_to_response(wb, u'中奖者名单')


def check_winners(request):
    data = request.POST

    award_id = data['name']
    award = Award.objects.filter(pk=award_id)

    status = award[0].status
    winners = Winner.objects.filter(award=award, remark=None)
    number = winners.count()

    winner_list = [{'name': item.staff.name, 'chineseName': item.staff.chineseName, 'avatar': item.staff.avatar} for
                   item in winners]
    return JsonResponse({'number': number, 'winner_list': winner_list, 'status': status})


def redraw_single_winner(request):
    """
    未报备且缺席人员重新抽奖
    """
    award_id = request.POST.get("award_id")
    winner_staff = request.POST.get("winner_staff")

    message = 'success'

    try:
        absent_winner = Staff.objects.get(name=winner_staff)
    except Staff.DoesNotExist:
        message = u'不存在staff为{}的人员'.format(winner_staff)
        return JsonResponse({'message': message, 'result': False})

    # 使缺席的人员中奖无效
    Winner.objects.filter(award=award_id, staff=absent_winner).update(remark=u'中奖无效')

    # 重新抽奖
    try:
        award = Award.objects.get(id=award_id)
    except Award.DoesNotExist:
        message = u'不存在的奖项'
        return JsonResponse({'message': message, 'result': False})

    if award.isAddToExclusion:
        ExclusionForAll.objects.create(staff=absent_winner)

    exclusions = [item.staff.name for item in Exclusion.objects.filter(award=award_id)]
    winners = []
    if award.everyoneCanDraw:
        exclusions.extend([item.staff.name for item in ExclusionForAll.objects.all()])
    else:
        winners = [item.staff.name for item in Winner.objects.all().exclude(remark__exact='forall')]

    staffs = Staff.objects.filter(staffList=absent_winner.staffList).exclude(name__in=exclusions).exclude(
        name__in=winners).values('id', 'name', 'chineseName', 'avatar', 'is_absent')

    if staffs.count() < 1:
        return JsonResponse({'message': u"抽奖无效，待抽奖人员为空", 'data': [], 'result': False})

    selected = random.sample(staffs, 1)[0]

    if selected['is_absent']:
        selected['chineseName'] = u"%s(报备)" % selected['chineseName']

    data = {'winner': selected}

    # 更新中奖人员
    new_winner = Winner(award_id=int(award_id), staff_id=selected['id'])
    new_winner.save()

    return JsonResponse({'message': message, 'data': data, 'result': True})
