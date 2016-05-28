#coding:utf-8
'''
Created on 2016年2月1日

@author: Warmer
'''
import time
from django.contrib.auth.hashers import make_password
from subject.settings import SSH_KEY, EMAIL_HOST_USER
from django.core.mail import send_mail

def time_control(req):
    deadline = time.localtime()
    if req.has_key('active'):
        return str(deadline[0])+str(deadline[1])+str(deadline[5]+deadline[4]*60+deadline[3]*60*60+(deadline[2])*24*60*60)
    elif req.has_key('regist'):
        return str(deadline[0])+str(deadline[1])+str(deadline[5]+deadline[4]*60+deadline[3]*60*60+(deadline[2]+7)*24*60*60)

'''
req = {'method':'active' || 'regist', 'username':   ,'email':   }
'''
def mail_control(req):
    userna = req['username']
    deadline = time_control({req['method']:''})
    unameDeadline = make_password(userna+deadline,None,SSH_KEY)
    activeURL = "smart.com/account/active/?name="+userna.decode('utf-8')+"&un="+unameDeadline+"&t="+deadline
    message = ("亲爱的"+userna+"，你好！\n感谢注册smart，请在7天内点击以下链接激活账号:\n").decode('utf-8')+activeURL
    send_mail("smart激活邮件",message,EMAIL_HOST_USER,[str(req['email'])])
    return unameDeadline