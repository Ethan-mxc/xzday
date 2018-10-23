#-*-coding:utf-8-*-
from django.core.mail import send_mail
def send_mymail(subject,body,send_to):
    print send_mail(subject,body, '18729580703@163.com', send_to, fail_silently=False)
    return 1
if __name__ == "__main__": 
    send_mymail('我是谁', '他', ['928099418@qq.com'])