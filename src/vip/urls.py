# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.conf.urls import url
from vip import views
app_name = 'vip'
urlpatterns = [
    url(r'^vipindex/$',views.vipindex,name = 'vipindex'),
    url(r'^vipsearch/$',views.vipsearch,name = 'vipsearch'),
    url(r'^vipchange/$',views.vipchange,name = 'vipchange'),
    url(r'^vipdelete/$', views.vipdelete, name='vipdelete'),
    url(r'^match/$',views.match,name='match')
]
