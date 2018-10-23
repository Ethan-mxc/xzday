#-*-coding:utf-8-*-
from tools.link import *
from online.models import *
from home.models import *
import time
def pingall():
    computes = Compute.objects.all()
    for compute in computes:
        if(ping_ip(compute.ip)):
            Compute.objects.filter(ip = compute.ip).update(state = "开机")
            try:
               activecompute = Compute.objects.get(ip = compute.ip)
            except:
                print 'err'
            else:
            
                if (activecompute.activetime!=None):
                    activetime = int(activecompute.activetime)+1
                    Compute.objects.filter(ip = compute.ip).update(activetime = str(activetime))
                else:
                    Compute.objects.filter(ip = compute.ip).update(activetime = '0')
        else:
            Compute.objects.filter(ip = compute.ip).update(state = "关机")
            try:
                idletcompute = Compute.objects.get(ip = compute.ip)
            except:
                print "err"
            else:
                if (idletcompute.idletime!=None):
                    idletime = int(idletcompute.idletime)+1
                    
                    Compute.objects.filter(ip = compute.ip).update(idletime = str(idletime))
                else:
                    Compute.objects.filter(ip = compute.ip).update(idletime = '0')
    return 1
def runpingall():
    while True:
       pingall()
       time.sleep(10) 
if __name__ == "__main__": 
    runpingall()
                
    