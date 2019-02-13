#-*-coding:utf-8-*-
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from tools.dbcon import *
from online.models import User
import json
import sys
import time
import  re
from django.views.decorators.cache import cache_page
reload(sys)
sys.setdefaultencoding('utf8')


#确定身份函数
def comfirm(req):
    if req.session['islogin'] == True:
        user_info = req.session['user_info']
        user_role = user_info['role']
        if user_role != '管理员':
            msg = '您不是管理员'
            return 0
        else:
            return 1

def index(req):
    if  comfirm(req):
        my_db = MynewcoderDB()
        sql = "select * from vip"
        infos = my_db.getInfo(sql)
        results = []
        for infos1_row in infos:
            results.append({'id':infos1_row[0],'vip':infos1_row[2]})
        sql_share = "select * from share"
        infos_share = my_db.getInfo(sql_share)
        resultsshare = []
        for infos_row in infos_share:
            resultsshare.append({'id':infos_row[0],'old':infos_row[1],'new':infos_row[2],'start_time':infos_row[3],'end_time':infos_row[4],'dingdanhao':infos_row[5],'invitation':infos_row[6],'change_time':infos_row[7]})
        my_db.close()
        return render(req,'index.html',locals())
    else:
        msg = "请求错误"
        return render(req,"msg.html", locals())


def vip_edit_action(req):
    if comfirm(req):#确认身份
        res_id = req.POST.get('res_id','0')
        res_vipid = req.POST.get('res_vipid','999999')
        res_mail = req.POST.get('res_mail','0')
        res_create_time = req.POST.get('res_create_time','2010-1-10')
        res_change_time = time.strftime('%Y-%m-%d %X', time.localtime() )
        res_deadline = req.POST.get('res_deadline','2020-1-1')
        my_db = MynewcoderDB()
        if res_id == '0':
            sql2 = "insert into vip (vipid,vip,create_time,change_time,deadline)values('" + res_vipid + "','" + res_mail + "','" + res_create_time + "','" + res_change_time + "','" + res_deadline + "')"
            infos2 = my_db.execute(sql2)
            my_db.commit()
            #已经存在的会员查询
            sql = "select * from vip"
            infos = my_db.getInfo(sql)
            results = []
            for infos1_row in infos:
                results.append({'id': infos1_row[0], 'vip': infos1_row[2]})
                #接下去是订单表查询
            sql_share = "select * from share"
            infos_share = my_db.getInfo(sql_share)
            resultsshare = []
            for infos_row in infos_share:
                resultsshare.append(
                    {'id': infos_row[0], 'old': infos_row[1], 'new': infos_row[2], 'start_time': infos_row[3],
                     'end_time': infos_row[4], 'dingdanhao': infos_row[5], 'invitation': infos_row[6],
                     'change_time': infos_row[7]})
            my_db.close()
            return render(req, 'index.html', locals())

        sql2 = "update vip set vipid='"+res_vipid+"' ,vip='"+res_mail+"', create_time ='"+res_create_time+"',change_time= '"+res_change_time+"',deadline='"+res_deadline+"' where id= '"+res_id+"' "
        infos2 = my_db.execute(sql2)
        my_db.commit()
        sql4 = "select * from vip where id ="+res_id+" "
        infos4 = my_db.getInfo(sql4)
        results = []
        for infos1_row in infos4:
            results.append(
                {'id': infos1_row[0], 'vipid': infos1_row[1], 'vip': infos1_row[2], 'create_time': infos1_row[3],
                     'change_time': infos1_row[4], 'deadline': infos1_row[5]})
        return render(req, 'member_edit.html', locals())
        my_db.close()
    else:
        msg = "请求错误"
        return render(req,"msg.html", locals())

def order_edit_action(req):
    if comfirm(req):#确认身份
        res_id = req.POST.get('id','0')
        res_old = req.POST.get('old','999999')
        res_new = req.POST.get('new','0')
        res_start_time = req.POST.get('start_time','2010-1-10')
        res_end_time = req.POST.get('end_time','2010-1-10')
        res_dingdanhao = req.POST.get('dingdanhao','2020-1-1')
        res_invitation = req.POST.get('invitation', '2020-1-1')
        res_change_time = time.strftime('%Y-%m-%d %X', time.localtime() )
        my_db = MynewcoderDB()
        if res_id == '0':
            sql2 = "insert into share (old,new,start_time,end_time,dingdanhao,invitation,change_time)values('" + res_old + "','" + res_new + "','" + res_start_time + "','" + res_end_time + "','" + res_dingdanhao + "','" + res_invitation + "','" + res_change_time + "')"
            infos2 = my_db.execute(sql2)
            my_db.commit()
            #已经存在的会员查询
            sql = "select * from share"
            infos = my_db.getInfo(sql)
            resultsshare = []
            for infos1_row in infos:
                resultsshare.append({'id': infos1_row[0], 'dingdanhao': infos1_row[5]})
                #接下去是订单表查询
            sql_share = "select * from vip"
            infos_share = my_db.getInfo(sql_share)
            results = []
            for infos_row in infos_share:
                results.append({'id': infos_row[0], 'vipid': infos_row[1], 'vip': infos_row[2], 'create_time': infos_row[3],'change_time': infos_row[4], 'deadline': infos_row[5]})
            my_db.close()
            return render(req, 'index.html', locals())

        sql3 = "update share set old='"+res_old+"', new ='"+res_new+"',start_time= '"+res_start_time+"',end_time='"+res_end_time+"',dingdanhao='"+res_dingdanhao+"',invitation='"+res_invitation+"',change_time='"+res_change_time+"' where id= '"+res_id+"' "
        infos3 = my_db.execute(sql3)
        my_db.commit()
        sql4 = "select * from share where id ="+res_id+" "
        infos4 = my_db.getInfo(sql4)
        results = []
        for infos_row in infos4:
            results.append(
                {'id': infos_row[0], 'old': infos_row[1], 'new': infos_row[2], 'start_time': infos_row[3],
                 'end_time': infos_row[4], 'dingdanhao': infos_row[5], 'invitation': infos_row[6],
                 'change_time': infos_row[7]})
        return render(req, 'share_edit.html', locals())
        my_db.close()
    else:
        msg = "请求错误"
        return render(req,"msg.html", locals())

def show(req,res_id):
    if comfirm(req):
        try:
            my_db = MynewcoderDB()
            sql = "select * from vip where id ="+res_id+" "
            infos = my_db.getInfo(sql)
            results = []
            for infos_row in infos:
                results.append({'id': infos_row[0], 'vipid': infos_row[1], 'vip': infos_row[2], 'create_time': infos_row[3],
                                'change_time': infos_row[4], 'deadline': infos_row[5]})
                my_db.close()
            return render(req,'member_edit.html',locals())
        except Exception as e:
            msg = '没有该信息，请重新查询'
            return render(req,"msg.html",locals())
    else:
        msg = "请求错误"
        return render(req,"msg.html", locals())

def order_show(req,res_id):
    if comfirm(req):
        try:
            my_db = MynewcoderDB()
            sql = "select * from share where id ="+res_id+" "
            infos = my_db.getInfo(sql)
            results = []
            for infos_row in infos:
                results.append({'id': infos_row[0], 'old': infos_row[1], 'new': infos_row[2], 'start_time': infos_row[3],
                     'end_time': infos_row[4], 'dingdanhao': infos_row[5], 'invitation': infos_row[6],
                     'change_time': infos_row[7]})
                my_db.close()
            return render(req,'share_edit.html',locals())
        except Exception as e:
            msg = '没有该信息，请重新查询'
            return render(req,"msg.html",locals())
    else:
        msg = "请求错误"
        return render(req,"msg.html", locals())

def search(req):
    if comfirm(req):
        try:
            text = req.POST['vip']
            my_db = MynewcoderDB()
            sql1 = "select * from vip where vip LIKE '%"+text+"%'"
            infos1 = my_db.getInfo(sql1)
            results = []
            for infos1_row in infos1:
                results.append({'id':infos1_row[0],'vipid':infos1_row[1],'vip':infos1_row[2],'create_time':infos1_row[3],'change_time':infos1_row[4],'deadline':infos1_row[5]})
            my_db.close()
            return render(req,'member_edit.html',locals())
        except Exception as e:
            msg = '没有该信息，请重新查询'
            return render(req,"msg.html",locals())
    else:
        msg = "请求错误"
        return render(req,"msg.html", locals())

def share_search(req):
    if comfirm(req):
        try:
            text = req.POST['share_dingdanhao']
            my_db = MynewcoderDB()
            sql1 = "select * from share where dingdanhao ='"+text+"'"
            infos1 = my_db.getInfo(sql1)
            results = []
            for infos_row in infos1:
                results.append({'id': infos_row[0], 'old': infos_row[1], 'new': infos_row[2], 'start_time': infos_row[3],
                     'end_time': infos_row[4], 'dingdanhao': infos_row[5], 'invitation': infos_row[6],
                     'change_time': infos_row[7]})
            my_db.close()
            return render(req,'share_edit.html',locals())
        except Exception as e:
            msg = '没有该信息，请重新查询'
            return render(req,"msg.html",locals())
    else:
        msg = "请求错误"
        return render(req, "msg.html", locals())

def vip_edit(req,res_id):
    if comfirm(req):#确认身份
        if str(res_id) == '0':
            return render(req,'vip_edit.html')
        try:
            my_db = MynewcoderDB()
            sql1 = "select * from vip where id = "+res_id+" "
            infos1 = my_db.getInfo(sql1)
            results = []
            for infos1_row in infos1:
                results.append({'id':infos1_row[0],'vipid':infos1_row[1],'vip':infos1_row[2],'create_time':infos1_row[3],'change_time':infos1_row[4],'deadline':infos1_row[5]})
            my_db.close()
            res = results[0]
            return render(req,'vip_edit.html',locals())
        except Exception as e:
            msg = '没有该信息，请重新查询'
            return render(req,"msg.html",locals())
    else:
        msg = "请求错误"
        return render(req,"msg.html", locals())

def order_edit(req,res_id):
    if comfirm(req):#确认身份
        if str(res_id) == '0':
            return render(req,'order_edit.html')
        try:
            my_db = MynewcoderDB()
            sql1 = "select * from share where id = "+res_id+" "
            infos1 = my_db.getInfo(sql1)
            results = []
            for infos_row in infos1:
                results.append({'id': infos_row[0], 'old': infos_row[1], 'new': infos_row[2], 'start_time': infos_row[3],
                     'end_time': infos_row[4], 'dingdanhao': infos_row[5], 'invitation': infos_row[6],
                     'change_time': infos_row[7]})
            my_db.close()
            res = results[0]
            return render(req,'order_edit.html',locals())
        except Exception as e:
            msg = '没有该信息，请重新查询'
            return render(req,"msg.html",locals())
    else:
        msg = "请求错误"
        return render(req,"msg.html", locals())

def delete(req,res_id):
    if comfirm(req):
        try:
            my_db = MynewcoderDB()
            #vip表的删除
            sql1 = "delete from vip where id ="+res_id+" "
            my_db.execute(sql1)
            my_db.commit()
            #############
            sql = "select * from vip"
            infos = my_db.getInfo(sql)
            results = []
            for infos1_row in infos:
                results.append({'id':infos1_row[0],'vipid':infos1_row[1],'vip':infos1_row[2],'create_time':infos1_row[3],'change_time':infos1_row[4],'deadline':infos1_row[5]})
            ####################
            sql_share = "select * from share"
            infos_share = my_db.getInfo(sql_share)
            resultsshare = []
            for infos_row in infos_share:
                resultsshare.append(
                    {'id': infos_row[0], 'old': infos_row[1], 'new': infos_row[2], 'start_time': infos_row[3],
                     'end_time': infos_row[4], 'dingdanhao': infos_row[5], 'invitation': infos_row[6],
                     'change_time': infos_row[7]})
            my_db.close()
            return render(req,"index.html",locals())
        except Exception as e:
            msg = '没有找到相关信息'
            return render(req,"msg",locals())
    else:
        msg = "请求错误"
        return render(req,"msg.html", locals())

def order_delete(req,res_id):
    if comfirm(req):
        try:
            my_db = MynewcoderDB()
            #vip表的删除
            sql1 = "delete from share where id ="+res_id+" "
            my_db.execute(sql1)
            my_db.commit()
            #####################
            sql = "select * from share"
            infos = my_db.getInfo(sql)
            resultsshare = []
            for infos_row in infos:
                resultsshare.append({'id': infos_row[0], 'old': infos_row[1], 'new': infos_row[2], 'start_time': infos_row[3],
                     'end_time': infos_row[4], 'dingdanhao': infos_row[5], 'invitation': infos_row[6],
                     'change_time': infos_row[7]})
            #####################
            sql_share = "select * from vip"
            infos_share = my_db.getInfo(sql_share)
            results = []
            for infos1_row in infos_share:
                results.append(
                    {'id':infos1_row[0],'vipid':infos1_row[1],'vip':infos1_row[2],'create_time':infos1_row[3],'change_time':infos1_row[4],'deadline':infos1_row[5]})
            my_db.close()
            return render(req,"index.html",locals())
        except Exception as e:
            msg = '没有找到相关信息'
            return render(req,"msg",locals())
    else:
        msg = "请求错误"
        return render(req,"msg.html", locals())
