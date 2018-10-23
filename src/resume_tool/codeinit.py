# -*- coding:utf-8 -*-
import MySQLdb
import jieba.posseg as pseg
import jieba.analyse as ana
import jieba
import re
#数据库相关
class MynewcoderDB:
    def __init__(self):
        self.db_conn= MySQLdb.connect(
        host='118.24.92.135',
        port = 3306,
        user='meng',
        passwd='123456',
        db ='newcoder',
        charset='utf8',
        )
        self.db_cur = self.db_conn.cursor()
    def execute(self,sqlstr):
        self.db_cur.execute(sqlstr)
    def getInfo(self,sqlstr):
        sqlstr = sqlstr.decode("utf-8")
        self.execute(sqlstr)
        return self.db_cur.fetchall()
    def commit(self):
        self.db_conn.commit()
    def close(self):
        self.db_cur.close()
        self.db_conn.close()

class WordCut:
    def __init__(self,sentence):
        self.sentence = sentence
    def cutWords(self):
        self.words = pseg.cut(self.sentence)
        return self.words
    def top(self,num=100):
        words = ana.extract_tags(self.sentence,num)
        return words
class Info:
    def __init__(self):
        jieba.load_userdict("words.txt")
    def getAlllist(self,sqlstr):
        self.my_db = MynewcoderDB()
        infos =  self.my_db.getInfo(sqlstr)
        
        for key in infos:
            self.id = key[0]
            self.findCode(key[1]+key[4])
    def findCode(self,infostr):
        pass
        
#邀请码相关
class InviteCode(Info):
    def __init__(self,usestr="内推码"):
        Info.__init__(self)
        self.usestr = usestr
        sqlstr = "SELECT * from discuss WHERE context like '%"+self.usestr+"%' OR title like '%"+self.usestr+"%'"
        self.getAlllist(sqlstr)
        
        #找到分词中邀请码最近的eng属性的词汇就是邀请码or内推码的内容
    def findCode(self,infostr):
        wordcut = WordCut(infostr)
        minilen = 1000
        i = 0
        lcyflagi = 0
        code = ""
        mycompany = ""
        for word, flag in wordcut.cutWords():
            i = i + 1
            if cmp(flag,"company")==0:
                mycompany = word
            if cmp(flag,"lcy")==0:
                lcyflagi = i
            if cmp(flag,"eng")==0:
                if (i-lcyflagi)<minilen:
                    minilen = i-lcyflagi
                    code = word
                if lcyflagi == 0:
                    continue
        if code!="" and lcyflagi!=0 and len(code)>6:
            print self.id,mycompany,code
    
#类型相关
class TypeOffer(Info):
    def __init__(self):
        Info.__init__(self)
        sqlstr = "SELECT * from discuss"
        self.getAlllist(sqlstr)
        
    def findCode(self,infostr):
        wordcut = WordCut(infostr)
        mycompanylist = []
        for word, flag in wordcut.cutWords():
            if cmp(flag,"company")==0:
                mycompanylist.append(word)
        if(len(mycompanylist)>0 and len(infostr)>2000):
            print self.id
            for mycom in mycompanylist:
                print mycom
                
                
                
        
            
            
        
        
        
    
        
        
        
        

if __name__=="__main__":
    icode = TypeOffer()
