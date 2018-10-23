#-*-coding:utf-8-*-
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from tools.dbcon import *
from online.models import User
import sys  
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
            return  render(req,"payindex.html")
        else:
            msg = '请登录'
            return render(req,'msg.html', locals())
def setjian(req):
        if req.method == 'POST':
            try:
                text=req.POST.get("text",'')
                intr=req.POST.get("intr",'')
                myinfo = text.split()
                comp = myinfo[1]
                local = myinfo[3]
                gw = myinfo[5]
                my_db = MynewcoderDB()
                sqlstr = "SELECT * from pay where 公司   = '"+comp+"' and 地点  = '"+local+"' and 岗位  = '"+gw+"' and 说明  ='"+intr+"'"
                myinfos = my_db.getInfo(sqlstr)
                mynum = int(myinfos[0][4])
                mynum = mynum-1
                sqlstr = "Update pay SET 可信度 = "+str(mynum)+" where 公司   = '"+comp+"' and 地点  = '"+local+"' and 岗位  = '"+gw+"' and 说明  ='"+intr+"'"
                my_db.execute(sqlstr)
                my_db.commit()
                my_db.close()
                msg = "点评成功"
                return HttpResponse(msg)
            except Exception,e:
                print e
                msg = "输入错误，请联系管理员"
                return HttpResponse(msg)
            else:
                msg = "点评成功"
                return HttpResponse(msg)       
def setjia(req):
    if req.method == 'POST':
            try:
                text=req.POST.get("text",'')
                intr=req.POST.get("intr",'')
                myinfo = text.split()
                comp = myinfo[1]
                local = myinfo[3]
                gw = myinfo[5]
                my_db = MynewcoderDB()
                sqlstr = "SELECT * from pay where 公司   = '"+comp+"' and 地点  = '"+local+"' and 岗位  = '"+gw+"' and 说明  ='"+intr+"'"
                myinfos = my_db.getInfo(sqlstr)
                mynum = int(myinfos[0][4])
                mynum = mynum+1
                sqlstr = "Update pay SET 可信度 = "+str(mynum)+" where 公司   = '"+comp+"' and 地点  = '"+local+"' and 岗位  = '"+gw+"' and 说明  ='"+intr+"'"
                my_db.execute(sqlstr)
                my_db.commit()
                my_db.close()
                msg = "点评成功"
                return HttpResponse(msg)
            except Exception,e:
                print e
                msg = "输入错误，请联系管理员"
                return HttpResponse(msg)
            else:
                msg = "点评成功"
                return HttpResponse(msg)          
    
def getpay(req):
    if req.method == 'POST':
        user_info = req.session['user_info']
        condition = {'name': user_info['name']}
        r = User.objects.get(**condition)
        if r.beans<5:
            msg = '用户豆不够，请充值'
            return render(req,'msg.html', locals())
        else:
            try:
                text=req.POST.get("paytext",'') 
                my_db = MynewcoderDB()
                sqlstr =  "SELECT * from pay where 公司   like '%"+text+"%' OR 地点  like '%"+text+"%' OR 岗位  like '%"+text+"%' ORDER BY 可信度   DESC  limit 10 "
                print sqlstr
                infos = my_db.getInfo(sqlstr)
                beans = r.beans - 5
                User.objects.filter(name=user_info['name']).update(beans=beans)
                req.session['beans'] = beans
                my_db.close()
                return render(req,"payindex.html",locals())
            except Exception,e:
                print e
                msg = "输入错误，请联系管理员"
                return render(req,'msg.html', locals())
            else:
                return render(req,"payindex.html",{'infos':infos})

