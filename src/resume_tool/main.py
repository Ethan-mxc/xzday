# -*- coding: utf-8 -*-

import sys
import os

import doc2txt as d2t
import pdf2txt as p2t
import html2txt as h2t
import eml2txt as e2t
import chardet
import email

import re

from tools import *
addsys()

# 获取一个文件夹内包括子文件夹所有doc文件的名字和路径
def getalldocfilename(path):
    docfilenames = []
    for dirpath, dirnames, filenames in os.walk(path):
        filenames = filter(
            lambda filename: (filename[-4:] == '.doc' or filename[-5:] == '.docx' or filename[-4:] == '.DOC'),
            filenames)
        filenames = map(lambda filename: os.path.join(dirpath, filename), filenames)
        docfilenames.extend(filenames)
        return docfilenames


# 获取一个文件夹内包括子文件夹所有pdf文件的名字和路径
def getallpdffilename(path):
    pdffilenames = list()
    for dirpath, dirnames, filenames in os.walk(path):
        filenames = filter(lambda filename: filename[-4:] == '.pdf', filenames)
        filenames = map(lambda filename: os.path.join(dirpath, filename), filenames)
        pdffilenames.extend(filenames)
        return pdffilenames


# 获取一个文件夹内包括子文件夹所有html文件的名字和路径
def getallhtmlfilename(path):
    htmlfilenames = []
    for dirpath, dirnames, filenames in os.walk(path):
        filenames = filter(
            lambda filename: (filename[-5:] == '.html' or filename[-4:] == '.htm'),
            filenames)
        filenames = map(lambda filename: os.path.join(dirpath, filename), filenames)
        htmlfilenames.extend(filenames)
        return htmlfilenames


# 获取一个文件夹内包括子文件夹所有pdf文件的名字和路径
def getallemlfilename(path):
    emlfilenames = list()
    for dirpath, dirnames, filenames in os.walk(path):
        filenames = filter(lambda filename: (filename[-4:] == '.eml' or filename[-4:] == '.mht'), filenames)
        filenames = map(lambda filename: os.path.join(dirpath, filename), filenames)
        emlfilenames.extend(filenames)
        return emlfilenames


def handle_document(filename):
    if (filename[-4:] == '.doc' or filename[-5:] == '.docx' or filename[-4:] == '.DOC'):
        content = d2t.handle_docfiles(filename)
    elif (filename[-4:] == '.pdf'):
        content = p2t.handle_pdffiles(filename)
    elif (filename[-5:] == '.html' or filename[-4:] == '.htm'):
        content = h2t.handle_htmlfiles(filename)
    elif (filename[-4:] == '.eml' or filename[-4:] == '.mht'):
        content = e2t.handle_emlfiles(filename)
    return content

def runall(path):
    docfile_list = getalldocfilename(path)  # 获取文件夹内所有文件的名字和路�?    pdffile_list = getallpdffilename(path)
    htmlfile_list = getallhtmlfilename(path)
    emlfile_list = getallemlfilename(path)

    # 将所有word文档转换为txt格式,引用封装的doc2txt模块
    for docfile in docfile_list:
        if docfile[-4:] == '.DOC':
            doc_file = docfile[:-4] + '.doc'
        else:
            doc_file = docfile
        d2t.convert_doc_to_txt(doc_file)

    # 将所有pdf文档转换为txt格式，引用封装的pdf2txt模块
    for pdffile in pdffile_list:
        # print pdffile
        pdf2t = pdffile[:-4]  # 以后缀.pdf切词
        f = open(pdf2t + '.txt', 'w+')  # 以txt格式保存
        f.write(p2t.convert_pdf_to_txt(pdffile))
        f.close()

    # 将所有html文档转换为txt格式
    for htmlfile in htmlfile_list:
        html2t = htmlfile[:-5]
        fout = open(html2t + '.txt', 'w')
        fin = open(htmlfile, 'r')
        strfile = fin.read()
        # print chardet.detect(strfile)
        # 文本格式的编码方式统一为utf-8
        if (chardet.detect(strfile)['encoding'] == 'GB2312'):
            str_file = h2t.html2text(strfile.decode("gbk", 'ignore').encode("utf-8", 'ignore'))
        if ((chardet.detect(strfile)['encoding'] == 'utf-8') or (chardet.detect(strfile)['encoding'] == 'UTF-8-SIG')):
            str_file = h2t.html2text(strfile)
        for t in str_file:
            txt = re.sub(r'[# * | -]?', '', t)  # drop #*
            fout.write(txt)
        fout.close()

    # 将所有email文档转换为txt格式
    for emlfile in emlfile_list:
        fp = open(emlfile, "r")
        msg = email.message_from_file(fp)# 创建消息对象
        email2t = emlfile[:-4]
        fout = open(email2t + '.txt', 'w')
        emltext = 'content:{}'.format(e2t.convert_eml_to_txt(msg))
        # print chardet.detect(emltext)
        if (chardet.detect(emltext)['encoding'] == 'GB2312'):
            str_file = h2t.html2text(emltext.decode("gbk", 'ignore').encode("utf-8", 'ignore'))
        if ((chardet.detect(emltext)['encoding'] == 'utf-8') or (chardet.detect(strfile)['encoding'] == 'UTF-8-SIG')):
            str_file = h2t.html2text(emltext)
        print str_file
        for t in str_file:
            txt = re.sub(r'[# * | ]?', '', t)  # drop #*
            fout.write(txt)
        fout.close()
        
if __name__ == '__main__':
    filename = r"C:\Users\Administrator\Desktop\jiuye0624\jiuye\src\resume_tool\1111114������ҵ��ѧ-��С��-˶ʿ-����ý��רҵ��.doc"
    path = sys.path[0]
    print path
    filename = path+"\\1111114������ҵ��ѧ-��С��-˶ʿ-����ý��רҵ��.doc"
    #runall(path)
    print filename
    handle_document(filename.decode('utf-8','ignore'))
