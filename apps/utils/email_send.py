#-*- encodeing:utf-8 -*-
#发送邮件
from random import Random

from django.core.mail import send_mail #发送邮件

from users.models import EmailVerifyRecoed
from mxonline.settings import DEFAULT_FROM_EMAIL

def random_str(randomlength=8):
    #生成随机字符串
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

def send_register_email(email,send_type = "register"):
    email_record = EmailVerifyRecoed()
    #生成随机16位的字符串
    random_code = random_str(16)
    email_record.code =random_code
    email_record.email = email
    email_record.send_type = send_type
    #保存验证码到数据库
    email_record.save()

    email_title = ""
    email_content = ""
    if send_type == "register":
        email_title = "墓穴王用户注册激活链接"
        email_content = "请点击下面的链接激活你的账号: http://127.0.0.1:8000/active/{0}".format(random_code)
        send_status =  send_mail(email_title,email_content,DEFAULT_FROM_EMAIL,[email])
        if send_status:
            pass

    elif send_type == "reset":
        email_title = "墓穴王用户充值密码链接"
        email_content = "请点击下面的链接重置你的账号密码: http://127.0.0.1:8000/reset/{0}".format(random_code)
        send_status =  send_mail(email_title,email_content,DEFAULT_FROM_EMAIL,[email])
        if send_status:
            pass



