#-*-coding:utf-8-*-
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from tools.dbcon import *
from online.models import User
import json
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
            return  render(req,"com_index.html", locals())
        else:
            msg = '请登录'
            return render(req,'msg.html', locals())
    if req.method == 'POST':
        msg = "模式错误"
        return  render(req,"msg.html", locals())  
            
    
def info(req):
    if req.method == 'POST' or req.method =='GET':
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
                else:
                    text = req.GET.get('comtext')
                my_db = MynewcoderDB()
                sqlstr =  "SELECT * from company where 标题   like '%"+text+"%'"
                infos = my_db.getInfo(sqlstr)
                compintr = infos[0]
                infos = infos[0]
                info = infos[1]
                jstemp = ['百度', '腾讯', '阿里巴巴']
                jsdtemp = [[84, 66, 1000, '百度', '百度'], [88, 60, 1000, '腾讯', '腾讯'], [86, 64, 1000, '阿里巴巴', '阿里巴巴']]
                try:
                    jsname = json.dumps(jstemp)
                    data = [float(compintr[8]) * 20, float(compintr[9]) * 20, 1000, compintr[1], compintr[1]]
                    if not compintr[1] in jstemp:
                        jsdtemp.append(data)
                        jstemp.append(compintr[1])
                    jsdata = json.dumps(jsdtemp)
                except:
                    pass
                beans = r.beans - 0
                User.objects.filter(name=user_info['name']).update(beans=beans)
                req.session['beans'] = beans
                my_db.close()
                return  render(req,"com_index.html", locals())  
            except Exception,e:
                msg = '没有该公司，请重新查询'
                return render(req,"msg.html", locals())

