#-*-coding:utf-8-*-
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from tools.dbcon import *
from online.models import User
from collections import Counter
import json
import sys
import time  
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
            return  render(req, "question_index.html")
        else:
            msg = '请登录'
            return render(req,'msg.html', locals())

#读大段然后内存处理
def info(req):
    if req.method == 'GET':
        data = ['review-frontend','acm-solutions','review-java','front-end-interview','nine-chapter']
        type = req.GET.get('type')
        if type == None:
            type = '1'
        page = req.GET.get('page')
        if page == None:
            page = '1'
        sqlstr = "select * from question where type = '"+data[int(type)]+"' limit "+str(int(page)-1)+",1"
        countsqlstr = "select * from question  where type = '"+data[int(type)] +"'"
        queinfo = que_sql(sqlstr)
        maxnumber = len(que_sql(countsqlstr))
        maxlist = []
        pagenumber = int(page)
        maxlist.append(1)
        if maxnumber>3:
            if pagenumber < 3:
                maxlist.append(2)
                maxlist.append(3)
            elif pagenumber > maxnumber-2:
                maxlist.append(maxnumber-2)
                maxlist.append(maxnumber-1)
            else:
                for i in range(pagenumber-1,pagenumber+2):
                    maxlist.append(i)
            maxlist.append(maxnumber)
        else:
            number = maxnumber
            for i in range(1,number+1):
                maxlist.append(i)
        print maxlist
    return  render(req, "question_info.html", locals())  

def list(req):
    if req.method == 'GET':
        data = ['review-frontend','acm-solutions','review-java','front-end-interview','nine-chapter']
        type = req.GET.get('type')
        if type == None:
            type = '1'
        sqlstr = "select * from question where type = '"+data[int(type)]+"'"
        data = que_sql(sqlstr)
    return  render(req, "question_list.html", locals())  

def que_sql(sqlstr,):
    my_db = MynewcoderDB()
    infos = my_db.getInfo(sqlstr)
    print sqlstr
    my_db.close()
    return infos       
        



