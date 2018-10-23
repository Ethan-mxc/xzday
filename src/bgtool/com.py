__author__ = 'corey'
# -*- coding:utf-8 -*-
import urllib
import urllib2
import re,json
from bs4 import BeautifulSoup
import requests
import MySQLdb

def changekey(key):
    return key.strip().replace("'",'"')

def get(url):
    try:
        request = urllib2.Request(url)
        #request.add_header('Pragma', 'no-cache')
        response = urllib2.urlopen(request,timeout=20)
        page = response.read()
        return page
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
        try:
            #标题
            self.title = soup.find("h1",{"class":"discuss-title"})
            self.title = soup.h1.get_text().strip()
            #作者
            louzhu =soup.find("span",{"class":"post-name"})
            louzhu = louzhu.find("a")
            self.louzhu = louzhu.attrs['title']
            self.louzhu = changekey(self.louzhu)

            #时间
            lztime =soup.find("span",{"class":"post-time"})
            lztime = lztime.get_text()
            lztime = lztime.split()
            self.lztime = lztime[1]+" "+lztime[2]
            self.lztime = changekey(self.lztime)

            #发表内容
            context =soup.find("div",{"class":"post-topic-des"})
            context = context.get_text()
            context = context.split()
            self.context = context[0]
            for i in range(1,len(context)-2):
                self.context = self.context+context[i]
            self.context = changekey(self.context)
        #pattern = re.compile('h1 class="discuss-title".*')
        #items = re.findall(pattern,page)
        #print items
            
            
        #评论数
            num = soup.findAll("h1")
            num = num[2].get_text()
            num = num.encode("utf-8")
            num = re.findall(r'(\w*[0-9]+)\w*',num)
            self.num = int(num[0])
            return True
        except:
            return False

        
    def getComPage(self,page):
        #最多pagesize是100
        #https://www.nowcoder.com/comment/list-by-page-v2?pageSize=200000&page=1&order=1&entityId=62719&entityType=8
        url = "https://www.nowcoder.com/comment/list-by-page-v2?pageSize=100&page="+str(page)+"&order=1&entityId="+str(self.Pindex)+"&entityType="+str(8);
        return get(url)
    
    def getComments(self,pageid):
        ids = []
        subcom= []
        compage = self.getComPage(pageid)
        #每次主回复的消息
        self.compage =json.loads(compage)
        #回复的子回复，每次的深度最多为1
        if self.num>100:
            num = 100
        else:
            num = self.num
        for i in range(0,num):
            ids.append(self.compage['data']['comments'][i]['id'])
        self.ids = ids
        for idtemp in ids:
            subcom.append(json.loads(self.getID(idtemp)))
        self.subcom = subcom
            

    def getID(self,idindex):
        #https://www.nowcoder.com/comment/list-by-page-v2?token=&pageSize=10&page=1&order=1&entityId=1091685&entityType=2&_=1511231131699
        url = "https://www.nowcoder.com/comment/list-by-page-v2?token=&pageSize=100&page=1&order=1&entityId="+str(idindex)+"&entityType=2"
        return get(url)
    def save(self,sqlstr):
        self.db_conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='liu',
        passwd='123456',
        db ='newcoder',
        charset='utf8',
        )
        
        self.db_cur = self.db_conn.cursor()
        try:
            
            self.db_cur.execute(sqlstr)
        except:
            print "error"   
        self.db_cur.close()
        self.db_conn.commit()
        self.db_conn.close()
        
    def saveall(self):
        #保存标题等
        sqlstr = "insert into discuss values('"+str(self.Pindex)+"','"+self.title+"','"+self.louzhu+"','"+self.lztime+"','"+self.context+"','"+str(self.num)+"')"
        self.save(sqlstr)
        
        #保存一级评论
        if self.num >100:
            num = 100
        else:
            num = self.num
        for i in range (0,num):
            sqlstr = "insert into comment values('"+str(self.Pindex)+"','0','"+str(self.compage['data']['comments'][i]['id'])+"','"+self.compage['data']['comments'][i]['authorName']+"','"+str(self.compage['data']['comments'][i]['authorId'])+"','"+self.compage['data']['comments'][i]['content']+"')"
            self.save(sqlstr)
        
        #保存二级评论
        for i in range (0,len(self.subcom)):
            for j in range (0,int(self.subcom[i]["data"]["totalCnt"])):
                print i,j
                sqlstr = "insert into comment values('"+str(self.Pindex)+"','"+str(self.subcom[i]['data']['comments'][j]['toCommentId'])+"','"+str(self.subcom[i]['data']['comments'][j]['id'])+"','"+self.subcom[i]['data']['comments'][j]['authorName']+"','"+str(self.subcom[i]['data']['comments'][j]['authorId'])+"','"+self.subcom[i]['data']['comments'][j]['content']+"')"
                self.save(sqlstr)
            
            
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

        for i in range(176046,900000):
            self.db_conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='liu',
        passwd='123456',
        db ='newcoder',
        charset='utf8',
        )
        
            self.db_cur = self.db_conn.cursor()
            self.getUser(i)
            self.db_cur.close()
            self.db_conn.commit()
        self.db_conn.close()
    def getAllContents(self):
        for i in range(100,10000):
            try:
                istrue = self.getContents(i)
                #大于100的必须分开
                count = 1;
                if istrue:
                    print i
                    while(self.num>100):
                        self.getComments(count)
                        self.saveall()
                        count = count+1
                        self.num -=100
                    self.getComments(count)
                    self.saveall()
                        
                else:
                    print "跳过",i
            except:
                pass
        
            
            
import sys
stdout = sys.stdout
reload(sys)
sys.stdout = stdout
    
spider = Spider()
spider.getAllContents()

'''
spider.getContents(62186)

spider.getComments()

#spider.printall()
'''
