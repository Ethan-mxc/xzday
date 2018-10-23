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
def index(req):
    if req.method == 'GET':
        try:
            islogin = req.session['islogin']
        except Exception,e:
            msg = '请登录'
            return render(req,'msg.html', locals())
        if req.session['islogin'] == True:
            return  render(req,"school_index.html", locals())
        else:
            msg = '请登录'
            return render(req,'msg.html', locals())
    if req.method == 'POST':
        msg = "模式错误"
        return  render(req,"msg.html", locals())


def all(req):
    if req.method == 'GET':
        user_info = req.session['user_info']
        condition = {'name': user_info['name']}
        r = User.objects.get(**condition)
        if r.beans < 1:
            msg = '用户豆不够，请充值'
            return render(req, 'msg.html', locals())
        else:
            try:
                text = req.GET.get("id", '')
                my_db = MynewcoderDB()
                sqlstr = "SELECT * from school where id   = "+text
                infos = my_db.getInfo(sqlstr)[0]
                beans = r.beans - 0
                User.objects.filter(name=user_info['name']).update(beans=beans)
                req.session['beans'] = beans
                my_db.close()
                return render(req, "school_all.html", locals())
            except Exception, e:
                msg = '没有该信息，请重新查询'
                return render(req, "msg.html", locals())

#@cache_page(60 * 5)
def info(req):
    user_info = req.session['user_info']
    condition = {'name': user_info['name']}
    r = User.objects.get(**condition)
    if r.beans<1:
        msg = '用户豆不够，请充值'
        return render(req,'msg.html', locals())
    else:
        try:
            if req.method == 'POST':
                text=req.POST.get("comtext",'')
                zw=req.POST.get("zw",'')
                fl=req.POST.get("fl",'')
            else:
                text = req.GET.get("comtext")
                if text == None:
                    text = ""
                zw = req.GET.get("zw")
                if zw == None:
                    zw = ""
                fl = ""
            my_db = MynewcoderDB()
            sqlstr =  "SELECT * from school where 公司   like '%"+text+"%'and 职位 like '%"+zw+"%' and 分类 like '%"+fl+"%' order by id DESC limit 10"
            infos = my_db.getInfo(sqlstr)
            beans = r.beans - 0
            User.objects.filter(name=user_info['name']).update(beans=beans)
            req.session['beans'] = beans
            my_db.close()
            return  render(req,"school_index.html", locals())
        except Exception,e:
            msg = '没有该信息，请重新查询'
            return render(req,"msg.html", locals())


def test_one(req):
    my_db = MynewcoderDB()
    sqlstr0 = "SELECT * from school where 职位   like '%测试%'"
    infos0 = my_db.getInfo(sqlstr0)
    num0 = 0
    for maindata in range(len(infos0)):
        num0 += 1
    sqlstr1 = "SELECT * from school where 职位   like '%数据%'"
    infos1 = my_db.getInfo(sqlstr1)
    num1 = 0
    for maindata in range(len(infos1)):
        num1 += 1
    sqlstr2 = "SELECT * from school where 职位   like '%java%'"
    infos2 = my_db.getInfo(sqlstr2)
    num2 = 0
    for maindata in range(len(infos2)):
        num2 += 1
    sqlstr3 = "SELECT * from school where 职位   like '%游戏%'"
    infos3 = my_db.getInfo(sqlstr3)
    num3 = 0
    for maindata in range(len(infos3)):
        num3 += 1
    sqlstr4 = "SELECT * from school where 职位   LIKE  '%测试%'  "
    infos4 = my_db.getInfo(sqlstr4)
    my_db.close()
    jsdata1 = ['数据','java','游戏','测试']
    jsdata2 = [num0, num1, num2, num3]
    return render(req,'test_one.html',locals())
