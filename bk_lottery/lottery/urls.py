# -*- coding: utf-8 -*-
from django.conf.urls import include, url

from . import views

urlpatterns = (
    url(r'^award/([0-9]+)/$', views.get_award_view),
    url(r'^award/([0-9]+)/update/$', views.set_award_prize),
    url(r'^award/([0-9]+)/winners/$', views.select_all_winners_by_award),

    url(r'^award/more/$', views.get_draw_again_view),  # 再抽一次

    url(r'^check_status/$', views.check_status),
    url(r'^check_winners/$', views.check_winners),


    url(r'^winners/$', views.get_winners_view),
    url(r'^winners/all/$', views.get_all_winners),
    url(r'^winners/download/$', views.download_winners_list),
    url(r'^redraw/$', views.redraw_single_winner),
)
