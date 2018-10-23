# -*- coding:utf8 -*-

import sys
import logging
import chardet
from tools import  *

addsys()


# Load MS Word document,change to txt and return the document object  #import win32com
def convert_doc_to_txt(file):  # takes in a filename and returns a word document object
    try:
        logging.debug('Converting word to txt: ' + str(file))
        wordapp = win32com.client.Dispatch('Word.Application')
        wordapp.Visible = False
        # 后缀名doc切词
        if file[-4:] == '.doc':
            doc2t = file[:-4]
        elif file[-5:] == '.docx':
            doc2t = file[:-5]
        print file
        wordapp.Documents.Open(file, False, False)# FileName, ConfirmConversions, ReadOnly
        wordapp.ActiveDocument.SaveAs(doc2t, FileFormat=2)
        wordapp.ActiveDocument.Close()
        fin = open(doc2t + '.txt', 'r')
        strfile = fin.read()
        #print strfile
        return strfile

    except Exception, e:
        logging.error('Error in file: ' + str(e))
        return ""


# 将word文档转换为txt格式
def handle_docfiles(docfile):
    if docfile[-4:] == '.DOC':
        doc_file = docfile[:-4] + '.doc'
    else:
        doc_file = docfile
    convert_doc_to_txt(doc_file)
