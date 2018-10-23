# -*- coding:utf8 -*-
import platform
def addsys():
    import sys #这里只是一个对sys的引用，只能reload才能进行重新加载
    stdi,stdo,stde=sys.stdin,sys.stdout,sys.stderr 
    reload(sys) #通过import引用进来时,setdefaultencoding函数在被系统调用后被删除了，所以必须reload一次
    sys.stdin,sys.stdout,sys.stderr=stdi,stdo,stde 
    sys.setdefaultencoding('utf-8')
    
def get_os(): 
  os = platform.system() 
  if os == "Windows": 
    return "n"
  else: 
    return "c"