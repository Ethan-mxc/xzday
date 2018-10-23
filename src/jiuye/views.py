'''
Created on 2018-1-4

@author: corey
'''
#-*-coding:utf-8-*-
import xlrd
from django.shortcuts import render
from django.template.context_processors import request
import sys
def indexView(req):
    return render(req,'baseindex.html',locals())

def more(req):
    return render(req,'moreindex.html',locals())

def page_not_found(req):
    return render(req,'404.html')