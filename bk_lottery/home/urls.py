#coding=utf-8
from django.conf.urls import url
from . import views

urlpatterns = (
    url(r'^$', views.get_home_views),
    url(r'^guide$', views.get_guide_view),
)
