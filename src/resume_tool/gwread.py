#!/usr/bin/env python
# encoding:utf-8
import sys
from codeinit import *
import jieba
import xlrd
reload(sys)
sys.setdefaultencoding('utf8')
input_encode = 'utf-8'
# 构建专业知识库

# 抽取技能信息,并将日期按照顺序排列存入list
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
             if word not in word_dict:
                 word_dict[word] = 10
             else:
                 word_dict[word] += 10

    import operator
    word_dict =  sorted(word_dict.items(), key=operator.itemgetter(1))
    for ktemp,vtemp in word_dict:
        print ktemp,vtemp

def readexcel(keyword,filename = "lagou.xls"):
    book = xlrd.open_workbook(filename)#得到Excel文件的book对象，实例化对象
    sheet0 = book.sheet_by_index(0) # 通过sheet索引获得sheet对象
    nrows = sheet0.nrows    # 获取行总数
    ncols = sheet0.ncols    #获取列总数
    words = ""
    for i in range(0,nrows):
        print i
        row_data = sheet0.row_values(i)     # 获得第1行的数据列表
        if row_data[0] == keyword:
            words = words+row_data[11]
    word_extract(words)


def run():
    readexcel("测试")
run()