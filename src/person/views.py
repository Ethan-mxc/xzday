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
import xlrd
reload(sys)  
sys.setdefaultencoding('utf-8')
def index(req):
    if req.method == 'GET':
        qz = 1
        req.session['qz'] = 1
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
                return  render(req, "person_index.html",locals())
            else:
                jl = 1
                return render(req, "person_index.html", locals())
        else:
            msg = '请登录'
            return render(req,'msg.html', locals())

def index2(req):
    if req.method == 'GET':
        qz = 0
        req.session['qz'] = 0
        try:
            islogin = req.session['islogin']
        except Exception, e:
            msg = '请登录'
            return render(req, 'msg.html', locals())

        if req.session['islogin'] == True:
            user_info = req.session['user_info']
            condition = {'name': user_info['name']}
            r = User.objects.get(**condition)
            if r.myresume != None and len(r.myresume) != 0:
                return render(req, "person_index.html", locals())
            else:
                jl = 1
                return render(req, "person_index.html", locals())
        else:
            msg = '请登录'
        return render(req, 'msg.html', locals())
#读大段然后内存处理
def info(req):
    if req.method == 'POST':
        qz = req.session['qz']
        try:
            comp = req.POST['comp']
        except:
            comp = ""
        try:
            job = req.POST['job']
        except:
            job = ""
        try:
            becomp = req.POST['becomp']
        except:
            becomp = ""
        try:
            bejob = req.POST['bejob']
        except:
            bejob = ""
        edu = req.POST['edu']
        major = req.POST['major']
        degree = req.POST['degree']

        email=req.session['user_info']['email']
        sqlstr = "INSERT INTO querylog (email,comp,job,becomp,bejob,edu,major,degree) VALUES ('"+email+"','"+ comp+"','"+job+"','"+becomp+"','"+bejob+"','"+edu+"','"+major+"','"+degree+"')"
        my_db = MynewcoderDB()
        infos = my_db.execute(sqlstr)
        my_db.commit()
        my_db.close()

        
        
        comp_list = []
        pos_list = []
        degree_list = []
        edu_list = []
        major_list = []
        detail_list = []
        myedunum = 0
        #该大学去的最多岗位和公司,公司UI和岗位UI
        if len(edu)!=0:
            import random
            key = random.randint(1,30000)
            keynum = random.randint(200,1000)
        
            #为空测试结果一致
            sqlstr = "select bz_job.company,bz_job.position from bz_job where bz_job.name in (select name from bz_edu where bz_edu.edu like '%"+edu.encode("utf-8")+"%' and bz_edu.major like '%"+major.encode("utf-8")+"%' and bz_edu.degree like '%"+degree+"%')"
            eduinfo = person_sql(sqlstr)
            if len(eduinfo)<200:
               sqlstr = "select bz_job.company,bz_job.position from bz_job where bz_job.name in (select name from bz_edu where bz_edu.edu like '%"+edu.encode("utf-8")+"%' and bz_edu.degree like '%"+degree.encode("utf-8")+"%')"
               eduinfo = person_sql(sqlstr)
               if len(eduinfo)<200:
                    sqlstr = "select bz_job.company,bz_job.position from bz_job where bz_job.name in (select name from bz_edu where bz_edu.degree like '%"+degree.encode("utf-8")+"%') limit "+str(key)+","+str(keynum)
                    eduinfo = person_sql(sqlstr)
            for tcomp,tpos in eduinfo:
                if len(tcomp) != 0:
                    comp_list.append(tcomp)
                if len(tpos) != 0:
                    pos_list.append(tpos)  
            compnumber = int(len(eduinfo)*3*3.14)
            pos_data,pos_num,pos_t_data,pos_t_num = data_single_handle(pos_list)
            comp_data,comp_num,comp_t_data,comp_t_num = data_single_handle(comp_list)
            
        if len(comp)!=0:
            #该公司的统计信息
            sqlstr = "select bz_edu.degree, bz_edu.edu ,bz_edu.major from bz_edu where bz_edu.name in (select name from bz_job where bz_job.company like '%" + comp.encode("utf-8") + "%' and bz_job.position like '%" + job.encode("utf-8") + "%')"
            compinfo = person_sql(sqlstr)
            if len(compinfo)<200:
               sqlstr = "select bz_edu.degree, bz_edu.edu ,bz_edu.major from bz_edu where bz_edu.name in (select name from bz_job where bz_job.company like '%" + comp.encode("utf-8") + "%')"
               compinfo = person_sql(sqlstr)
            edunumber = int(len(compinfo)*3*3.14)
              
            for td,te,tm in compinfo:
                if len(td) != 0:
                    degree_list.append(td)
                if len(te) != 0:
                    edu_list.append(te)
                if len(tm) != 0:
                    major_list.append(tm)
            degree_list = change_dic(degree_list)
            a = {}
            if len(edu)!=0:
                templist = Counter(edu_list)            
                myedunum = templist[edu]
                a['name'] = edu
                a['value'] = int(myedunum*3.14*3)   
            edu_list = change_dic(edu_list)
            if len(a)!=0 and myedunum!=0:
                edu_list.pop(-1)
                edu_list.append(a)
            degree_t_data = degree_list
            degree_data = json.dumps(degree_list) 
                              
            major_data,major_num,major_t_data,major_t_num = data_single_handle(major_list)
            major_list = change_dic(major_list)
            
            #该公司以前的人都去哪了，即关联公司
            sqlstr = "select company,count(company) from bz_job where name in (select bz_job.name from bz_job where bz_job.company like '%"+ comp.encode("utf-8")+"%') and bz_job.company not like '%"+ comp.encode("utf-8")+"%'  group by company ORDER BY COUNT(company) DESC LIMIT 5"
            lcomp_data,lcomp_num,lcomp_t_data,lcomp_t_num,lcomp_number = data_handle(sqlstr)
            #这是个人项目经历
            if len(edu)!=0:
                num = 4
                tcount = 0
                while(num):
                    tcount = tcount+1
                    sqlstr = "select * from bz_job where bz_job.name in (SELECT * FROM (select bz_job.name from bz_job,bz_edu where bz_job.company like '%"+comp.encode("utf-8")+"%' and bz_edu.edu like '%"+edu+"%' and bz_edu.name=bz_job.name ORDER BY  bz_job.time desc limit "+str(tcount)+",1) AS s)"
                    detailinfo = person_sql(sqlstr)
                    if len(detailinfo)>1 and len(detailinfo)<10:
                        detail_list.append(detailinfo)
                        num = num -1
                    if tcount > 20:
                        break
            
        if len(job)!=0:    
            sqlstr = "select position,count(position) from bz_job where bz_job.position!='' and name in (select bz_job.name from bz_job where bz_job.position like '%"+ job.encode("utf-8")+"%') and bz_job.position not like '%"+ job.encode("utf-8")+"%'  group by position ORDER BY COUNT(position) DESC LIMIT 5"
            ljob_data,ljob_num,ljob_t_data,ljob_t_num,ljob_number= data_handle(sqlstr)
            sqlstr = "select position from bz_job where bz_job.position!='' and name in (select bz_job.name from bz_job where bz_job.position like '%"+ job.encode("utf-8")+"%') and bz_job.position not like '%"+ job.encode("utf-8")+"%'  group by position ORDER BY COUNT(position)"
            ljob_number = int(len(person_sql(sqlstr))*3.14*3)
        if len(becomp)!=0:
            sqlstr = "select company,count(company) from bz_job where bz_job.company!='' and name in (select bz_job.name from bz_job where bz_job.company like '%"+ becomp.encode("utf-8")+"%') and bz_job.company not like '%"+ becomp.encode("utf-8")+"%'  group by company ORDER BY COUNT(company) DESC LIMIT 5"
            bcomp_data,bcomp_num,bcomp_t_data,bcomp_t_num,bcomp_number = data_handle(sqlstr)
            if len(comp)!=0:
                sqlstr = "select company from bz_job where bz_job.company!='' and name in (select bz_job.name from bz_job where bz_job.company like '%" + becomp.encode(
                "utf-8") + "%') and bz_job.company like '%" + comp.encode("utf-8") + "%' "
                print sqlstr
                tempnumber = int(len(person_sql(sqlstr)) * 3.14 * 3)
                if comp not in bcomp_t_data:
                    bcomp_t_data.append(comp)
                    bcomp_t_num.append(tempnumber)
                    bcomp_data = json.dumps(bcomp_t_data)
                    bcomp_num = json.dumps(bcomp_t_num)



            sqlstr = "select company from bz_job where bz_job.company!='' and name in (select bz_job.name from bz_job where bz_job.company like '%"+ becomp.encode("utf-8")+"%') and bz_job.company not like '%"+ becomp.encode("utf-8")+"%'"
            bcomp_number = int(len(person_sql(sqlstr)) * 3.14 * 3)
        if len(bejob)!=0:
            sqlstr = "select position,count(position) from bz_job where bz_job.position!='' and name in (select bz_job.name from bz_job where bz_job.position like '%"+ bejob.encode("utf-8")+"%') and bz_job.position not like '%"+ bejob.encode("utf-8")+"%' group by position ORDER BY COUNT(position) DESC LIMIT 5"
            bjob_data,bjob_num,bjob_t_data,bjob_t_num,bjob_number = data_handle(sqlstr)
            sqlstr = "select position from bz_job where bz_job.position!='' and name in (select bz_job.name from bz_job where bz_job.position like '%"+ bejob.encode("utf-8")+"%') and bz_job.position not like '%"+ bejob.encode("utf-8")+"%'"
            bjob_number = int(len(person_sql(sqlstr)) * 3.14 * 3)
        #缺少验证信息
        return  render(req, "person_info.html", locals()) 


#这个方法直接sql全部处理完    
def test(req):
    if req.method == 'GET':  
        comp = req.GET.get('comp')
        if comp == None:
            comp = ""
        job = req.GET.get('job')
        if job == None:
            job = ""
        edu = req.GET.get('edu')
        if edu == None:
            edu = ""
        major = req.GET.get('major')
        if major == None:
            major = ""
        degree = req.GET.get('degree')
        if degree == None:
            degree = ""
        becomp =req.GET.get('becomp')
        if becomp == None:
            becomp = ""
        bejob = req.GET.get('bejob')
        if bejob == None:
            bejob = ""
        comp_list = []
        pos_list = []
        degree_list = []
        edu_list = []
        major_list = []
        detail_list = []
        myedunum = 0
        #该大学去的最多岗位和公司,公司UI和岗位UI
        if len(edu)!=0:
            import random
            key = random.randint(1,30000)
            keynum = random.randint(200,1000)
        
            #为空测试结果一致
            sqlstr = "select bz_job.company,bz_job.position from bz_job where bz_job.name in (select name from bz_edu where bz_edu.edu like '%"+edu.encode("utf-8")+"%' and bz_edu.major like '%"+major.encode("utf-8")+"%' and bz_edu.degree like '%"+degree+"%')"
            eduinfo = person_sql(sqlstr)
            if len(eduinfo)<200:
               sqlstr = "select bz_job.company,bz_job.position from bz_job where bz_job.name in (select name from bz_edu where bz_edu.edu like '%"+edu.encode("utf-8")+"%' and bz_edu.degree like '%"+degree.encode("utf-8")+"%')"
               eduinfo = person_sql(sqlstr)
               if len(eduinfo)<200:
                    sqlstr = "select bz_job.company,bz_job.position from bz_job where bz_job.name in (select name from bz_edu where bz_edu.degree like '%"+degree.encode("utf-8")+"%') "
                    eduinfo = person_sql(sqlstr)
            for tcomp,tpos in eduinfo:
                if len(tcomp) != 0:
                    comp_list.append(tcomp)
                if len(tpos) != 0:
                    pos_list.append(tpos)  
            compnumber = int(len(eduinfo)*3*3.14)
            pos_data,pos_num,pos_t_data,pos_t_num = data_single_handle(pos_list)
            comp_data,comp_num,comp_t_data,comp_t_num = data_single_handle(comp_list)
            
        if len(comp)!=0:
            sqlstr = "select * from company where 标题 like '%" + comp.encode("utf-8") + "%'"
            compintr = person_sql(sqlstr)
            compintr = compintr[0]
            jstemp = ['百度','腾讯','阿里巴巴']
            jsdtemp =[[84,66,1000,'百度','百度'],[88,60,1000,'腾讯','腾讯'],[86,64,1000,'阿里巴巴','阿里巴巴']]

            try:
                jsname = json.dumps(jstemp)
                data = [float(compintr[8]) * 20, float(compintr[9]) * 20, 1000, compintr[1], compintr[1]]
                if not compintr[1] in jstemp:
                    jsdtemp.append(data)
                    jstemp.append(compintr[1])
                jsdata = json.dumps(jsdtemp)
            except:
                compintr = []
            #该公司的统计信息
            sqlstr = "select bz_edu.degree, bz_edu.edu ,bz_edu.major from bz_edu where bz_edu.name in (select name from bz_job where bz_job.company like '%" + comp.encode("utf-8") + "%' and bz_job.position like '%" + job.encode("utf-8") + "%')"
            compinfo = person_sql(sqlstr)
            if len(compinfo)<200:
               sqlstr = "select bz_edu.degree, bz_edu.edu ,bz_edu.major from bz_edu where bz_edu.name in (select name from bz_job where bz_job.company like '%" + comp.encode("utf-8") + "%')"
               compinfo = person_sql(sqlstr)
            edunumber = int(len(compinfo)*3*3.14)
              
            for td,te,tm in compinfo:
                if len(td) != 0:
                    degree_list.append(td)
                if len(te) != 0:
                    edu_list.append(te)
                if len(tm) != 0:
                    major_list.append(tm)
            degree_list = change_dic(degree_list)
            a = {}
            if len(edu)!=0:
                templist = Counter(edu_list)            
                myedunum = templist[edu]
                a['name'] = edu
                a['value'] = int(myedunum*3.14*3)   
            edu_list = change_dic(edu_list)
            if len(a)!=0 and myedunum!=0:
                edu_list.pop(-1)
                edu_list.append(a)
            degree_t_data = degree_list
            degree_data = json.dumps(degree_list)
                              
            major_data,major_num,major_t_data,major_t_num = data_single_handle(major_list)
            major_list = change_dic(major_list)
            
            #该公司以前的人都去哪了，即关联公司
            sqlstr = "select company,count(company) from bz_job where name in (select bz_job.name from bz_job where bz_job.company like '%"+ comp.encode("utf-8")+"%') and bz_job.company not like '%"+ comp.encode("utf-8")+"%'  group by company ORDER BY COUNT(company) DESC LIMIT 5"
            lcomp_data,lcomp_num,lcomp_t_data,lcomp_t_num,lcomp_number = data_handle(sqlstr)
            sqlstr = "select company from bz_job where name in (select bz_job.name from bz_job where bz_job.company like '%"+ comp.encode("utf-8")+"%') and bz_job.company not like '%"+ comp.encode("utf-8")+"%'"
            lcomp_number = int(len(person_sql(sqlstr))*3.14*3) 
            #这是个人项目经历
            if len(edu)!=0:
                num = 4
                tcount = 0
                while(num):
                    tcount = tcount+1
                    sqlstr = "select * from bz_job where bz_job.name in (SELECT * FROM (select bz_job.name from bz_job,bz_edu where bz_job.company like '%"+comp.encode("utf-8")+"%' and bz_edu.edu like '%"+edu+"%' and bz_edu.name=bz_job.name ORDER BY  bz_edu.time desc limit "+str(tcount)+",1) AS s)"
                    detailinfo = person_sql(sqlstr)
                    if len(detailinfo)>1 and len(detailinfo)<10:
                        detail_list.append(detailinfo)
                        num = num -1
                    if tcount > 20:
                        while(num):
                            sqlstr = "select * from bz_job where bz_job.name in (SELECT * FROM (select bz_job.name from bz_job,bz_edu where bz_job.company like '%"+comp.encode("utf-8")+"%' and bz_edu.degree like '%"+degree+"%' and bz_edu.name=bz_job.name ORDER BY  bz_edu.time desc limit "+str(tcount)+",1) AS s)"
                            detailinfo = person_sql(sqlstr)
                            tcount = tcount+1
                            if len(detailinfo)>1 and len(detailinfo)<10:
                                detail_list.append(detailinfo)
                                num = num -1
                            if tcount >100:
                                num = 0
                                break
            sqlstr =  "select position  from bz_job where position!='' and bz_job.name in (select bz_job.name from bz_job,bz_edu where bz_job.company like '%" + comp.encode("utf-8") + "%' and bz_edu.edu like '%" + edu.encode("utf-8") + "%' and bz_job.name = bz_edu.name)"
            test_number = int(len(person_sql(sqlstr))*3.14*3)
            
            if test_number<200*3.14*3:
                sqlstr =  "select position  from bz_job where position!='' and bz_job.name in (select bz_job.name from bz_job,bz_edu where bz_job.company like '%" + comp.encode("utf-8") + "%' and bz_edu.degree like '%" + degree.encode("utf-8") + "%' and bz_job.name = bz_edu.name )"
                test_number = int(len(person_sql(sqlstr))*3.14*3)              
                sqlstr =  "select position,count(position) from bz_job where position!='' and bz_job.name in (select bz_job.name from bz_job,bz_edu where bz_job.company like '%" + comp.encode("utf-8") + "%' and bz_edu.degree like '%" + degree.encode("utf-8") + "%') group by position ORDER BY COUNT(position) DESC LIMIT 5"
                test_data,test_num,test_t_data,test_t_num,testnumber = data_handle(sqlstr)
            else:
                sqlstr =  "select position,count(position) from bz_job where position!='' and bz_job.name in (select bz_job.name from bz_job,bz_edu where bz_job.company like '%" + comp.encode("utf-8") + "%' and bz_edu.edu like '%" + edu.encode("utf-8") + "%' and bz_job.name = bz_edu.name) group by position ORDER BY COUNT(position) DESC LIMIT 5"
                test_data,test_num,test_t_data,test_t_num,testnumber = data_handle(sqlstr)

            
        if len(job)!=0:    
            sqlstr = "select position,count(position) from bz_job where bz_job.position!='' and name in (select bz_job.name from bz_job where bz_job.position like '%"+ job.encode("utf-8")+"%') and bz_job.position not like '%"+ job.encode("utf-8")+"%'  group by position ORDER BY COUNT(position) DESC LIMIT 5"
            ljob_data,ljob_num,ljob_t_data,ljob_t_num,ljob_number= data_handle(sqlstr)

            
        if len(becomp)!=0:
            sqlstr = "select company,count(company) from bz_job where bz_job.company!='' and name in (select bz_job.name from bz_job where bz_job.company like '%"+ becomp.encode("utf-8")+"%') and bz_job.company not like '%"+ becomp.encode("utf-8")+"%'  group by company ORDER BY COUNT(company) DESC LIMIT 5"
            bcomp_data,bcomp_num,bcomp_t_data,bcomp_t_num,bcomp_number = data_handle(sqlstr)
            sqlstr = "select company from bz_job where bz_job.company!='' and name in (select bz_job.name from bz_job where bz_job.company like '%"+ becomp.encode("utf-8")+"%') and bz_job.company not like '%"+ becomp.encode("utf-8")+"%'"
            bcomp_number = int(len(person_sql(sqlstr))*3*3.14)     
        
        if len(bejob)!=0:
            sqlstr = "select position,count(position) from bz_job where bz_job.position!='' and name in (select bz_job.name from bz_job where bz_job.position like '%"+ bejob.encode("utf-8")+"%') and bz_job.position not like '%"+ bejob.encode("utf-8")+"%' group by position ORDER BY COUNT(position) DESC LIMIT 5"
            bjob_data,bjob_num,bjob_t_data,bjob_t_num,bjob_number = data_handle(sqlstr)

        #添加了关键字浮动
        word_list =readexcel(comp)
        word_list = json.dumps(word_list)

        #添加了公司信息详情
        if len(comp)!=0:
            sqlstr ="select count(college_college.college_name) from bz_edu,college_college where bz_edu.name in (select name from bz_job where bz_job.company like '%"+comp+"%' and bz_job.position like '%"+job+"%') and bz_edu.edu = college_college.college_name GROUP BY college_college.isTwo;"
            twoinfo = person_sql(sqlstr)
            if len(twoinfo) == 1:
                sqlstr = "select count(college_college.college_name) from bz_edu,college_college where bz_edu.name in (select name from bz_job where bz_job.company like '%" + comp + "%') and bz_edu.edu = college_college.college_name GROUP BY college_college.isTwo;"
                twoinfo = person_sql(sqlstr)
            twodata = []
            twotemp = {}
            twotemp['name'] = "非211学校"
            twotemp['value'] = int(int(twoinfo[0][0])*3.14)
            twodata.append(twotemp)
            twotemp = {}
            twotemp['name'] = "211学校"
            twotemp['value'] = int(int(twoinfo[1][0])*3.14)
            twodata.append(twotemp)
            twodata = json.dumps(twodata)

            sqlstr ="select count(college_college.college_name) from bz_edu,college_college where bz_edu.name in (select name from bz_job where bz_job.company like '%"+comp+"%' and bz_job.position like '%"+job+"%') and bz_edu.edu = college_college.college_name GROUP BY college_college.isNine;"
            nineinfo = person_sql(sqlstr)
            if len(nineinfo) == 1:
                sqlstr = "select count(college_college.college_name) from bz_edu,college_college where bz_edu.name in (select name from bz_job where bz_job.company like '%" + comp + "%') and bz_edu.edu = college_college.college_name GROUP BY college_college.isNine;"
                nineinfo = person_sql(sqlstr)
            ninedata = []
            ninetemp = {}
            ninetemp['name'] = "非985学校"
            ninetemp['value'] = int(int(nineinfo[0][0])*3.14)
            ninedata.append(ninetemp)
            ninetemp = {}
            ninetemp['name'] = "985学校"
            ninetemp['value'] = int(int(nineinfo[1][0])*3.14)
            ninedata.append(ninetemp)
            ninedata = json.dumps(ninedata)

        excelFile = 'maindata.xls'
        data = xlrd.open_workbook(sys.path[0] + "//" + excelFile)
        table = data.sheets()[0]
        nrows = table.nrows
        ncols = table.ncols
        mainlist = []
        for i in xrange(nrows-100, nrows):
            rowValues = table.row_values(i)
            if str(rowValues[1]).find(str(comp))>=0:
                mainlist.append(rowValues)
        #缺少验证信息
        return  render(req, "person_info.html", locals()) 
    
def person_sql(sqlstr,):
    my_db = MynewcoderDB()
    infos = my_db.getInfo(sqlstr)
    my_db.close()
    return infos

def data_single_handle(comp_list):
    comp_data = []
    comp_num = []
    comp_list = change_dic(comp_list)
    for tdata in comp_list:
        comp_data.append(tdata['name'])
        comp_num.append(int(tdata['value']))
    temp_data = comp_data
    temp_num = comp_num
    comp_data = json.dumps(comp_data)
    comp_num = json.dumps(comp_num)
    return comp_data,comp_num,temp_data,temp_num  

def data_handle(sqlstr):
    data = []
    num = []
    beforeinfo = person_sql(sqlstr)
    number = int(len(beforeinfo)*3.14*3)
    for tdata,tnum in beforeinfo:
            data.append(tdata)
            num.append(int(tnum*3.14*3)) 
    tdata = data
    tnum = num
    data = json.dumps(data)
    num = json.dumps(num)
    return data,num,tdata,tnum,number

def change_dic(List):
    alist = []
    data =  Counter(List).most_common(5)
    for tdata,tnum in data:
        a = {}
        a['name'] = tdata
        a['value'] = int(tnum*3.14*3)
        alist.append(a)
    return alist

def word_extract(str):
    wordcut = WordCut(str)
    word_dict = {}
    for word, flag in wordcut.cutWords():

         if flag == "n" or flag == "vn":
             if word not in word_dict:
                 word_dict[word] = 1
             else:
                 word_dict[word] += 1
         if flag == "eng":
             word = word.upper()
             if word not in word_dict:
                 word_dict[word] = 10
             else:
                 word_dict[word] += 10

    import operator
    word_dict =  sorted(word_dict.items(), key=operator.itemgetter(1))
    word_list = []
    for ktemp,vtemp in word_dict:
        word = {}
        word['text'] = ktemp
        import random
        word['weight'] = int(vtemp)
        word_list.append(word)
    word_list=word_list[len(word_list)-20:-1]
    return word_list

def readexcel(keyword,filename = "lagou.xls"):
    book = xlrd.open_workbook(filename)#得到Excel文件的book对象，实例化对象
    sheet0 = book.sheet_by_index(0) # 通过sheet索引获得sheet对象
    nrows = sheet0.nrows    # 获取行总数
    ncols = sheet0.ncols    #获取列总数
    words = ""
    for i in range(0,nrows):
        row_data = sheet0.row_values(i)     # 获得第1行的数据列表
        if row_data[0] == keyword:
            words = words+row_data[11]
    return word_extract(words)


