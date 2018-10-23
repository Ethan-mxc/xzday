#-*-coding:utf-8-*-
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from tools.dbcon import *
from online.models import User
import json
import sys
import  re
from django.views.decorators.cache import cache_page
reload(sys)
sys.setdefaultencoding('utf8')

def vipindex(req):
    my_db = MynewcoderDB()
    sql = "select * from vip"
    infos = my_db.getInfo(sql)
    my_db.close()
    return render(req,'index.html',locals())

def vipsearch(req):
    try:
        if req.method == 'POST':
            text = req.POST.get("vip",'')
        else:
            text = req.GET.get("vip")
        my_db = MynewcoderDB()
        sql = "select * from vip where vip LIKE '%"+text+"%'"
        infos = my_db.getInfo(sql)
        my_db.close()
        return render(req,'index.html',locals())
    except Exception,e:
        msg = '没有该信息，请重新查询'
        return render(req,"msg.html",locals())

def vipchange(req):
    try:
        if req.method == 'POST':
            text = req.POST.get("id",'')
        else:
            text = req.GET.get("id")
        my_db = MynewcoderDB()
        sql = "select * from vip where vip LIKE '%"+text+"%'"
        infos = my_db.getInfo(sql)
        my_db.close()
        return render(req,'member_edit.html',locals())
    except Exception,e:
        msg = '没有该信息，请重新查询'
        return render(req,"msg.html",locals())

def vipdelete(req):
    try:
        if req.method == 'POST':
            text = req.POST.get("vip", '')
        else:
            text = req.GET.get("vip")
        my_db = MynewcoderDB()
        sql = "delete from vip like '%"+text+"%'"
        infos = my_db.execute(sql)
        my_db.commit()
        my_db.close()
        return render(req,"index.html",locals())
    except Exception,e:
        msg = '没有找到相关信息'
        return render(req,"msg",locals())
def match(req):
    my_db = MynewcoderDB()
    sql = "select * from vip WHERE  vip LIKE 'text'"
    infos = my_db.getInfo(sql)
    if infos==0:
        catch = 0
        return render(req,"index.html",{"nofound":"Doesn't exist"})
    else:
        catch = 1
        return render(req,"index.html",locals())

def invitation(req):
    pass
