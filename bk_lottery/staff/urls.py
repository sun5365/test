# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from . import views

urlpatterns = (
    url(r'^all/([0-9]+)/$', views.get_all_staff),
    url(r'^static/all/([0-9]+)/$', views.get_all_staff_as_js),

    url(r'^upload/$', views.save_staff_from_excel),
    url(r'^remove/$', views.remove_staff_by_staff_list),
    url(r'^remove/check/$', views.check_staff_list_can_remove),
)
