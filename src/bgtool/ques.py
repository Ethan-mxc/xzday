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
def hangkey(key):
    return key.replace("\n", "!")
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
            #����
            self.title = soup.find("h1",{"class":"discuss-title"})
            self.title = soup.h1.get_text().strip()
            #����
            louzhu =soup.find("span",{"class":"post-name"})
            louzhu = louzhu.find("a")
            self.louzhu = louzhu.attrs['title']
            self.louzhu = changekey(self.louzhu)

            #ʱ��
            lztime =soup.find("span",{"class":"post-time"})
            lztime = lztime.get_text()
            lztime = lztime.split()
            self.lztime = lztime[1]+" "+lztime[2]
            self.lztime = changekey(self.lztime)

            #��������
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
            
            
        #������
            num = soup.findAll("h1")
            num = num[2].get_text()
            num = num.encode("utf-8")
            num = re.findall(r'(\w*[0-9]+)\w*',num)
            self.num = int(num[0])
            return True
        except:
            return False

        
    def getComPage(self,page):
        #���pagesize��100
        #https://www.nowcoder.com/comment/list-by-page-v2?pageSize=200000&page=1&order=1&entityId=62719&entityType=8
        url = "https://www.nowcoder.com/comment/list-by-page-v2?pageSize=100&page="+str(page)+"&order=1&entityId="+str(self.Pindex)+"&entityType="+str(8);
        return get(url)
    
    def getComments(self,pageid):
        ids = []
        subcom= []
        compage = self.getComPage(pageid)
        #ÿ�����ظ�����Ϣ
        self.compage =json.loads(compage)
        #�ظ����ӻظ���ÿ�ε�������Ϊ1
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
        #��������
        sqlstr = "insert into discuss values('"+str(self.Pindex)+"','"+self.title+"','"+self.louzhu+"','"+self.lztime+"','"+self.context+"','"+str(self.num)+"')"
        self.save(sqlstr)
        
        #����һ������
        if self.num >100:
            num = 100
        else:
            num = self.num
        for i in range (0,num):
            sqlstr = "insert into comment values('"+str(self.Pindex)+"','0','"+str(self.compage['data']['comments'][i]['id'])+"','"+self.compage['data']['comments'][i]['authorName']+"','"+str(self.compage['data']['comments'][i]['authorId'])+"','"+self.compage['data']['comments'][i]['content']+"')"
            self.save(sqlstr)
        
        #�����������
        for i in range (0,len(self.subcom)):
            for j in range (0,int(self.subcom[i]["data"]["totalCnt"])):
                print i,j
                sqlstr = "insert into comment values('"+str(self.Pindex)+"','"+str(self.subcom[i]['data']['comments'][j]['toCommentId'])+"','"+str(self.subcom[i]['data']['comments'][j]['id'])+"','"+self.subcom[i]['data']['comments'][j]['authorName']+"','"+str(self.subcom[i]['data']['comments'][j]['authorId'])+"','"+self.subcom[i]['data']['comments'][j]['content']+"')"
                self.save(sqlstr)
            
            
    #����ҳ��Ҫ��¼���Ա�cookie֮���ִ��ڱ���t��¼��¼��Ϣ��postmanʵ��ɹ�
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
            #д�����ݿ� 
            sqlstr = "insert into NCuser values('"+str(userindex)+"','"+name+"','"+city+"','"+edu+"','"+intr+"','"+liv+"','"+cur+"','"+wor+"','"+el+"','"+com+"','"+job+"')"
            sqlstr = sqlstr.encode("utf-8")
            try:
                self.db_cur.execute(sqlstr)
                print name,city,edu,intr,liv,cur,wor,el,com,job

            except:
                print "error"
        else:
            print "����",userindex
    def getQA(self,pageid,QAtype):
        #https://www.nowcoder.com/ta/nine-chapter/review?page=2
        url = "https://www.nowcoder.com/ta/"+QAtype+"/review?tpId=1&query=&asc=true&order=&page="+str(pageid)
        page = get(url)
        soup = BeautifulSoup(page,"lxml")
        try:
            que = soup.find("div",{"class":"final-question"})
            que = que.get_text().strip()
            que = changekey(que)
        except:
            que = ""
        try:
            asw = soup.find("div",{"class":"design-answer-box"})
            asw = asw.get_text().strip()
            asw = changekey(asw)
        except:
            asw = ""

        
        sqlstr = "insert into question values('"+QAtype+"','"+que+"','"+asw+"','0')"
        self.save(sqlstr)
        
    def getcountQA(self,QAtype):
        url = "https://www.nowcoder.com/ta/"+QAtype+"/review?tpId=1&query=&asc=true&order=&page=1"
        page = get(url)
        soup = BeautifulSoup(page,"lxml")
        try:
            count = soup.find("button",{"class":"btn btn-primary js-pagination-jump"})
            count = count['data-total-page']
            self.count = int(count)
        except:
            self.count = 0
            
    def getAllQA(self):
        QAlist = ["review-frontend","acm-solutions","review-c","review-test","review-java","review-network","front-end-interview","nine-chapter"]
        for j in range(0,len(QAlist)):
            self.getcountQA(QAtype=QAlist[j])
            for i in range(1,self.count+1):
                print j,i
                self.getQA(i,QAtype=QAlist[j])
            
    def getAllUser(self):

        for i in range(176046,900000):
            self.db_conn= MySQLdb.connect(
        host='118.24.92.135',
        port = 3306,
        user='meng',
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
        for i in range(63516,66174):
            try:
                istrue = self.getContents(i)
                #����100�ı���ֿ�
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
                    print "����",i
            except:
                pass

        
            
            
import sys
stdout = sys.stdout
reload(sys)
sys.stdout = stdout
    
spider = Spider()
#spider.getAllQA()
spider.getAllContents()

'''
spider.getContents(62186)

spider.getComments()

#spider.printall()
'''
