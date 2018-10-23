#-*- coding: utf-8 -*- 

''''' 
不同平台，实现对所在内网端的ip扫描 
  
有时候需要知道所在局域网的有效ip，但是又不想找特定的工具来扫描。 
使用方法 python ip_scaner.py 192.168.1.1 
(会扫描192.168.1.1-255的ip) 
'''
  
import platform 
import sys 
import os 
import time 
import thread


    
def ping_ip(ip_str): 
    cmd = ["ping", "-{op}".format(op=get_os()), 
      "1", ip_str] #only one bag
    output = os.popen(" ".join(cmd)).readlines() 
    
    flag = False
    for line in list(output): 
       if not line: 
           continue
       if str(line).upper().find("TTL") >=0: 
           flag = True
           break
    if flag: 
        return True
    return False
    
if __name__ == "__main__": 
    print ping_ip("172.19.10.120")