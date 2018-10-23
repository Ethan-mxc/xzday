#-*-coding:utf-8-*-
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from tools.dbcon import *
from online.models import User
from resume_tool.run import *
from resume_tool.all_extractor2 import *
from resume_tool.main import *
from django.shortcuts import redirect

import json
import sys 
import random 
reload(sys)  
sys.setdefaultencoding('utf8') 

import os
  
def index(req):
    if req.method == 'GET':
        try:
            islogin = req.session['islogin']
        except Exception,e:
            msg = '请登录'
            return render(req,'msg.html', locals())
        
        if req.session['islogin'] == True:
            user_info = req.session['user_info']
            condition = {'name': user_info['name']}
            r = User.objects.get(**condition)
            if r.myresume != None and len(r.myresume)!=0:
                flag = 0
                result_list = process(r.myresume)
                info_list = result_list[0]
                ship_list = result_list[1]
                skill_list = result_list[2]
                project_list = result_list[3]
                socre_list = result_list[4]
                word_list = []
                for skill in skill_list:
                    word = {}
                    word['text'] = skill
                    word['weight'] = random.uniform(100, 1000)
                    word_list.append(word)
                word_list = json.dumps(word_list)
                return  render(req,"resumeindex.html", locals())
            else:
                flag = 1
                return  render(req,"resumeindex.html", locals())
        else:
            msg = '请登录'
            return render(req,'msg.html', locals())
        
def upload_file(req):  
    if req.method == "POST":    # 请求方法为POST时，进行处理  
        user_info = req.session['user_info']
        user_name = user_info['name']
        myFile =req.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None  
        if not myFile:  
            return HttpResponse("no files for upload!") 
        filename = ""
        if cmp(get_os(),"n")==0:
            filename = sys.path[0]+"\\"+user_name+myFile.name
        else:
            filename = sys.path[0]+"/"+user_name+myFile.name
        destination = open(filename,'wb+')    # 打开特定的文件进行二进制的写操作  
        for chunk in myFile.chunks():      # 分块写入文件  
            destination.write(chunk)  
        destination.close()
        print filename
        result_list,myresume = runresume(filename)
        User.objects.filter(name=user_name).update(myresume=myresume)
        info_list = result_list[0]
        ship_list = result_list[1]
        skill_list = result_list[2]
        project_list = result_list[3]
        socre_list = result_list[4]
        word_list = []
        for skill in skill_list:
            word = {}
            word['text'] = skill
            word['weight'] = random.uniform(100, 1000)
            word_list.append(word)
        word_list = json.dumps(word_list)
        return  render(req,"resumeindex.html", locals())

def upload_file_person(req):
    if req.method == "POST":    # 请求方法为POST时，进行处理
        user_info = req.session['user_info']
        user_name = user_info['name']
        myFile =req.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return HttpResponse("no files for upload!")
        filename = ""
        if cmp(get_os(),"n")==0:
            filename = sys.path[0]+"\\"+user_name+myFile.name
        else:
            filename = sys.path[0]+"/"+user_name+myFile.name
        destination = open(filename,'wb+')    # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()
        result_list,myresume = runresume(filename)
        User.objects.filter(name=user_name).update(myresume=myresume)
        return  HttpResponseRedirect("../../person/index")