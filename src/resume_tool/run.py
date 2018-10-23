# -*- coding: utf-8 -*-
from all_extractor2 import *
from main import *
import sys
def runresume(input):
    #处理多线程问题
    import pythoncom
    pythoncom.CoInitialize()
    handle_document(input.decode('utf-8','ignore'))
    filenames = input.split(".")
    filename = filenames[0]
    for i in range(1,len(filenames)-1):
        filename = filename+filenames[i]
    result_list = process(filename+'.txt')
    return result_list,filename+'.txt'
    
if __name__ == '__main__':
    filename = r"\1111114北京工业大学-李小龙-硕士-数字媒体专业历.doc"
    path = os.getcwd()
    runresume(path+filename)
    
