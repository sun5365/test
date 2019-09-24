# -*- coding: utf-8 -*-

from common.mymako import render_mako_context
from common.log import logger
from django.conf import settings

from lottery.models import Award, Plan
from home.models import AppMetaConfig

# Create your views here.


def get_home_views(request):
    """
    首页
    """
    message = ''
    result = False

    try:
        plan = Plan.objects.get(status=1)
        result = True
    except Plan.DoesNotExist as e:
        logger.error("plan: %s" % e)
        message = u'当前没有激活状态的方案或有多个激活状态的方案'
        plan = None

    awards = Award.objects.filter(plan=plan).order_by('sequence')
    return render_mako_context(request, '/home/home.html', {
        'awards': awards,
        'message': message,
        'result': result,
        })


def get_guide_view(request):
    """
    帮助页面
    """
    return render_mako_context(request, '/home/lottery_guides.html')
