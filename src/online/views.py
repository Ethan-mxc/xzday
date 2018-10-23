#encoding:utf-8
from django.shortcuts import render_to_response,render
from django.http import HttpResponseRedirect
from online.models import User
from django.template import RequestContext
import time
import smtplib
from email.mime.text import MIMEText
from django import forms
  
mail_host="smtp.163.com"  #设置服务器
mail_user="18309238981"    #用户名
mail_pass="19920203"   #口令 
mail_postfix="163.com"  #发件箱的后缀

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

def forget(req):
    pass 
 
def send_mail(to_list,sub,content):  
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"  
    msg = MIMEText(content,_subtype='plain',_charset='utf-8')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True  
    except Exception, e:  
        print str(e)  
        return False

def gotologin(req):
    if req.method == 'GET':
        return render(req,'login.html', locals())

def login(req):
    if req.method == 'GET':
        msg = '请求方式错误'
        return render(req, 'msg.html', locals())

    name = req.POST['name']
    passwd = req.POST['passwd']
    # 获取的表单数据与数据库进行比较
    condition = {'email': name}
    try:
        r = User.objects.get(**condition)
    except User.DoesNotExist:
        msg = "邮箱不存在，请先注册"
        return render(req,'user_register.html', locals())

    else:
        if r.passwd == passwd:
            req.session['islogin'] = True
            user_info = {}
            user_info['id'] = r.id
            user_info['name'] = r.name
            user_info['email'] = r.email
            user_info['role'] = r.role
            req.session['beans'] = r.beans
            req.session['head_image'] = r.head_image.name

            user_role = user_info['role']
            print user_role
            if user_role == '管理员':
                req.session['user_info'] = user_info
                msg = "登录成功！"
                return render(req, "manager_index.html", locals())
            elif user_role == '普通用户':
                req.session['user_info'] = user_info
                msg = "登录成功！"
                return HttpResponseRedirect('/school/index/')
            else:  # there are only 2 roles in system for now, will add 3rd role which is "Super user" in the future
                #                 req.session['user_info'] = user_info
                #                 msg = '您不是管理员'
                #                 return render(req,'msg.html', locals())
                return HttpResponseRedirect('/')  # for super user, will jump to super_user_index.html


                #             if(r.role == u"管理员"):
                #                 req.session['role']=True
                #             else:
                #                 req.session['role']=False
                #             req.session['user_info'] = user_info
                #             msg="登录成功！"
                #             return HttpResponseRedirect('/')
        else:
            msg = '密码错误！'
            return render(req, 'login.html', locals())
    
def logout(req):
    req.session['islogin'] = False
    req.session['user_info'] = {}
    return HttpResponseRedirect('/')


def register(req):
    if req.method == 'GET':
        status = False
        return render(req,'user_register.html', locals())
    else:
        status = True
        name = req.POST['aname']
        email = req.POST['email']
        passwd = req.POST['apasswd']
        graduate = req.POST['graduate']
        filterResult=User.objects.filter(name=name)
        emailfilterResult = User.objects.filter(email=email)
        if len(filterResult)>0:
            msg = '用户名被人注册过了！'
            return render(req, 'user_register.html', locals())
        if len(emailfilterResult)>0:
            msg = '邮箱被人注册过了！'
            return render(req, 'user_register.html', locals())
        User.objects.create(name= name,passwd=passwd,email=email,graduate=graduate,beans=1,role="普通用户",create_date=time.strftime('%Y-%m-%d %X', time.localtime() ))
        msg = '注册完成，请直接登录！'
        return render(req, 'login.html', locals())


def changepasswd(req):
    if not req.session['islogin']:
        msg = '你当前还没有登录，请先登录！'
        return render(req, 'login.html', locals())
    msg='changepasswd page'
    if req.method == 'GET':
        status = False
        return render(req,'changepasswd.html', locals())
    else:
        status=True
        passwd = req.POST['passwd']
        name = req.session['user_info']['name']
        User.objects.filter(name=name).update(passwd=passwd)
        req.session['islogin']=False
        msg="密码修改成功，请重新登录！"
        return render(req, 'login.html', locals())
    
def getpasswd(req):
    msg='getpasswd page'
    if req.method == 'GET':
        status = False
        return render(req,'getpasswd.html', locals())
    else:
        status=True
        name = req.POST['name']
        try:
            r = User.objects.get(name = name)
        except User.DoesNotExist:
            msg="用户名不存在，请先注册！"
            return render(req,'msg.html', locals())
        passwd = r.passwd
        email = r.email
        sub = "能耗管理系统密码找回"
        content = "您的密码是："+str(passwd)
        send_mail(email,sub,content)
        msg="密码已经发送到您的邮箱，请查收！"
        return render(req,'msg.html', locals())
    
def changehead_image(req):
    if req.method == 'GET':
        status = False
        return render_to_response('changehead_image.html', locals())
    if req.method == 'POST':
        form = ImageUploadForm( req.POST, req.FILES )  # 有文件上传要传如两个字段
        if form.is_valid():
            m = User.objects.get(name = req.session['user_info']['name'])
            m.head_image = form.cleaned_data['image']                     # 直接在这里使用 字段名获取即可
            m.save()
            req.session['head_image'] = m.head_image.name
            msg = "image upload success"
            return HttpResponseRedirect('/')
    msg = "allowed only via POST"
    return render_to_response('msg.html', locals())