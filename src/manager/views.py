#-*-coding:utf-8-*-
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from tools.dbcon import *
from online.models import User
from difflib import Match

import json
import sys  
import os
import resume_tool
import re
import time
import datetime
import xlrd

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
            user_info = req.session['user_info']
            user_role = user_info['role']
            if user_role == '管理员':
                return render(req, "manager_index.html", locals())
            else:
                msg = '您不是管理员'
                return render(req,'msg.html', locals())
        else:
            msg = '请登录'
            return render(req,'msg.html', locals())
    if req.method == 'POST':
        msg = "模式错误"
        return  render(req,"msg.html", locals())

def file_upload(req):
    t = time.time()
    time_now = time.strftime('%Y%m%d_%H%M%S', time.localtime(t))

    try:
        islogin = req.session['islogin']
    except Exception, e:
        msg = '请登录'
        return render(req, 'msg.html', locals())


    if req.session['islogin'] == True:
        user_info = req.session['user_info']
        user_role = user_info['role']
        if user_role != '管理员':
            msg = '您不是管理员'
            return render(req, 'msg.html', locals())

    if req.method == 'POST':
        excelin = req.FILES.get("excelin", None)
        print sys.path[0]       #D:\jiuye0320\jiuye\src
        if not excelin:  
            return HttpResponse("no files for upload!") 
        print excelin.name
        fileName = ""
        
        # 判断扩展名
        if re.search(r'.xlsx$', excelin.name) is not None:
            nameUnextended = excelin.name.split(".xlsx")[0]
            fileName = sys.path[0] + "\\" + "excelfiles\\" + nameUnextended + "_uploadDate_" + time_now + ".xlsx"
            destination = open(fileName,'wb+')    # 打开特定的文件进行二进制的写操作  
            for chunk in excelin.chunks():      # 分块写入文件  
                destination.write(chunk)  
            destination.close()
            print "xlsx"
        elif re.search(r'.xls$', excelin.name) is not None:
            nameUnextended = excelin.name.split(".xls")[0]
            fileName = sys.path[0] + "\\" + "excelfiles\\" + nameUnextended + "_uploadDate_" + time_now + ".xls"
            destination = open(fileName,'wb+')    # 打开特定的文件进行二进制的写操作  
            for chunk in excelin.chunks():      # 分块写入文件  
                destination.write(chunk)  
            destination.close()
            print "xls"
        else:# for later *.csv or other type file
            return HttpResponse("Wrong file extension! Please re-select file.")
        print fileName
        
        #read and write line by line from uploaded Excel files to DB
        #file I/O test
        xlsx_data = xlrd.open_workbook(fileName)
        table = xlsx_data.sheet_by_index(0)
        nrows = table.nrows
        ncols = table.ncols
        colnames = table.row_values(0)
        sql_args = ""
        print nrows,ncols
        for i in range(1,nrows):
            WorkList = []
            row = table.row_values(i)
            for j in range(0, ncols):
                if type(row[j]) == float:
                    row[j] = str(row[j])
                WorkList.append(row[j])
#             print WorkList[0] + ", " + WorkList[1]
            my_db = MynewcoderDB()
            for temp in range(0,len(WorkList)):
                WorkList[temp]=WorkList[temp].replace("\'","-");
            sql_query = "select * from school where "+" 采集日期='" + WorkList[0] + "' and 公司='" + WorkList[1] + "'and 职位='" + WorkList[2]+ "'and 职位描述='" + WorkList[3] + "'and 投递方式= '" + WorkList[4]+ "'and 分类='" + WorkList[5] + "'and 地点= '" + WorkList[6] + "'and URL= '" + WorkList[7] + "'"
            tempinfo = my_db.getInfo(sql_query)
            if tempinfo ==None or len(tempinfo)==0:
                sql_query = "REPLACE  INTO school  VALUES ('" + WorkList[0] + "','" + WorkList[1] + "','" + WorkList[2]+ "','" + WorkList[3] + "','" + WorkList[4] + "','" + WorkList[5] + "','" + WorkList[6]+ "','" + WorkList[7] + "'" +",0)"
            #the sql_query above may cause issue because the data from Excel file may contains '"' symbol
            #the '"' symbol may cause sql_query cannot be executed
            #print sql_query
                my_db.execute(sql_query)
                my_db.commit()
                WorkList = []#reset WorkList
            uploads = 1
        return  render(req,"manager_index.html", locals()) 

def bean_recharge(req):
    if req.session['islogin'] == True:
        user_info = req.session['user_info']
        user_role = user_info['role']
        if user_role != '管理员':
            msg = '您不是管理员'
            return render(req, 'msg.html', locals())

    if req.method == 'POST':
        recharge_user_name = req.POST['recharge_user_name']
        recharge_beans = req.POST['recharge_beans']
        
        user_beans = User.objects.get(email=recharge_user_name).beans
        pre_beans = user_beans#充值前校招豆数量
        
        recharge_beans_int = int(recharge_beans)
        user_beans += recharge_beans_int
        
        User.objects.filter(email=recharge_user_name).update(beans=user_beans)
        
        aft_beans = User.objects.get(email=recharge_user_name).beans#充值后校招豆数量
        u_beans = aft_beans - pre_beans#充值数量
        
        return render(req,"manager_index.html", {'u_beans': u_beans})
    
def authorize(req):
    if req.session['islogin'] == True:
        user_info = req.session['user_info']
        user_role = user_info['role']
        if user_role != '管理员':
            msg = '您不是管理员'
            return render(req, 'msg.html', locals())

    if req.method == 'POST':
        authorize_user_name = req.POST['authorize_user_name']
        pre_user_role = User.objects.get(name=authorize_user_name).role
        User.objects.filter(name=authorize_user_name).update(role='管理员')#authorize to manager
        user_role = User.objects.get(name=authorize_user_name).role
        if pre_user_role == user_role:
            auth_msg = '用户 ' + authorize_user_name + ' 已经是管理员'
        else:
            auth_msg = '用户 ' + authorize_user_name + ' 管理员权限授权成功'
        role_data = [0, auth_msg]
        return render(req,"manager_index.html", {'role_data': role_data})
