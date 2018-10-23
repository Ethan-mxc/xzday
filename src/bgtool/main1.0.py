__author__ = 'corey'
# -*- coding:utf-8 -*-
 
import urllib
import urllib2
import re,json
from bs4 import BeautifulSoup
import requests
import MySQLdb



def get(url):
    try:
        request = urllib2.Request(url)
        request.add_header('Pragma', 'no-cache')
        response = urllib2.urlopen(request,timeout=20)
        return response.read()
    except:
        return ""
class Spider:
 
    def __init__(self):
        self.siteURL = 'https://www.nowcoder.com/discuss/'

    def getPage(self,pageIndex):
        self.Pindex = pageIndex
        url = self.siteURL + str(pageIndex)+"?type=0&order=0&page=1"
        return get(url)

 
    def getContents(self,pageIndex):
        page = self.getPage(pageIndex)
        soup = BeautifulSoup(page,"lxml")
        #标题
        self.title = soup.find("h1",{"class":"discuss-title"})
        self.title = soup.h1.get_text()
        #作者
        louzhu =soup.find("span",{"class":"post-name"})
        louzhu = louzhu.find("a")
        self.louzhu = louzhu.attrs['title']

        #时间
        lztime =soup.find("span",{"class":"post-time"})
        lztime = lztime.get_text()
        lztime = lztime.split()
        self.lztime = lztime[1]+" "+lztime[2]

        #发表内容
        context =soup.find("div",{"class":"post-topic-des"})
        context = context.get_text()
        context = context.split()
        self.context = context[0]
        for i in range(1,len(context)-2):
            self.context = self.context+context[i]
        #pattern = re.compile('h1 class="discuss-title".*')
        #items = re.findall(pattern,page)
        #print items
            
        #评论数
        num = soup.findAll("h1")
        num = num[2].get_text()
        num = num.encode("utf-8")
        num = re.findall(r'(\w*[0-9]+)\w*',num)
        self.num = num[0]

        
    def getComPage(self):
        #https://www.nowcoder.com/comment/list-by-page-v2?pageSize=20&page=1&order=1&entityId=62719&entityType=8
        url = "https://www.nowcoder.com/comment/list-by-page-v2?page=1&order=1&entityId="+str(self.Pindex)+"&entityType="+str(8);
        return get(url)
    
    def getComments(self):
        num = int(self.num)
        ids = []
        subcom= []
        compage = self.getComPage()
        #每次主回复的消息
        self.compage =json.loads(compage)
        #回复的子回复，每次的深度最多为1
        for i in range(0,num):
            ids.append(self.compage['data']['comments'][i]['id'])
        self.ids = ids
        for idtemp in ids:
            subcom.append(json.loads(self.getID(idtemp)))
        self.subcom = subcom
            

    def getID(self,idindex):
        #https://www.nowcoder.com/comment/list-by-page-v2?token=&pageSize=10&page=1&order=1&entityId=1091685&entityType=2&_=1511231131699
        url = "https://www.nowcoder.com/comment/list-by-page-v2?token=&pageSize=10&page=1&order=1&entityId="+str(idindex)+"&entityType=2"
        return get(url)
    def printall(self):
        print self.title,self.louzhu,self.lztime,self.context,self.num,self.compage,self.ids,self.subcom
    #该网页需要登录，对比cookie之后发现存在变量t记录登录信息，postman实验成功
    def getUser(self,userindex):
        url = "https://www.nowcoder.com/profile/"+str(userindex)+"/basicinfo"
        try:
            opener = urllib2.build_opener()
            opener.addheaders.append(('Cookie', 't=C139A5266EFAE233DD9C9FC10C0A1B5C'))
            page = opener.open(url,timeout=20)
            soup = BeautifulSoup(page,"lxml")
            istrue = soup.find("div",{"class":"null-tip"})
        except:
            istrue = ""
        if istrue == None:
            try:
                name = soup.find("dd",{"id":"nicknamePart"})
                name = name.get_text().strip()
            except:
                name = ""
            try:
                city = soup.find("li",{"class":"profile-city"})
                city = city.get_text().strip()
            except:
                city = ""
            try:
                edu = soup.find("dd",{"id":"schoolInfoPart"})
                edu = edu.get_text().strip()
            except:
                edu = ""
            try:
                intr = soup.find("dd",{"id":"introductionPart"})
                intr = intr.get_text().strip()
            except:
                intr = ""
            try:
                liv = soup.find("dd",{"id":"livePlacePart"})
                liv =  liv.get_text().strip()
            except:
                liv = ""
            try:
                cur = soup.find("dd",{"id":"curIdentityPart"})
                cur = cur.get_text().strip()
            except:
                cur = ""
            try:
                wor = soup.find("dd",{"id":"workTimePart"})
                wor = wor.get_text().strip()
            except:
                wor = ""
            try:
                el = soup.find("dd",{"id":"eduLevelPart"})
                el =  el.get_text().strip()
            except:
                el = ""
            try:
                com = soup.find("dd",{"id":"companyInfoPart"})
                com = com.get_text().strip()
            except:
                com = ""
            try:
                job = soup.find("dd",{"id":"jobInfoPart"})
                job = job.get_text().strip()
            except:
                job = ""
            #写入数据库 
            sqlstr = "insert into NCuser values('"+str(userindex)+"','"+name+"','"+city+"','"+edu+"','"+intr+"','"+liv+"','"+cur+"','"+wor+"','"+el+"','"+com+"','"+job+"')"
            sqlstr = sqlstr.encode("utf-8")
            try:
                self.db_cur.execute(sqlstr)
                print name,city,edu,intr,liv,cur,wor,el,com,job

            except:
                print "error"
        else:
            print "跳过",userindex
            
    def getAllUser(self):

        for i in range(2000000,3000000):
            self.db_conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='liu',
        passwd='123456',
        db ='newcoder',
        charset='utf8',
        )
        
            self.db_cur = self.db_conn.cursor()
            print i
            self.getUser(i)
            self.db_cur.close()
            self.db_conn.commit()
        self.db_conn.close()
            
            
            
            
    
spider = Spider()
spider.getAllUser()

'''
spider.getContents(62186)

spider.getComments()

#spider.printall()
'''
