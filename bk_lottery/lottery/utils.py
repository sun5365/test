# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.utils.encoding import escape_uri_path, smart_unicode

from lottery.models import Plan, Award, Winner, Exclusion
from staff.models import Staff


def save_winners(staffs, award):
    winners = []
    Winner.objects.filter(award=award).update(remark=u'中奖无效')
    remark = "forall" if award.everyoneCanDraw else None
    for staff in staffs:
        winners.append(Winner(award=award, staff_id=staff['id'], remark=remark))
    Winner.objects.bulk_create(winners)


def xls_to_response(xls, filename):
    response = HttpResponse(content_type='application/ms-execl')
    response['Content-Disposition'] = "attachment; filename*=utf-8''{}.xls".format(escape_uri_path(filename))
    xls.save(response)
    return response
