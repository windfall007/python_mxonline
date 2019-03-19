#-*- encodeing:utf-8 -*-
from django.db import models
from datetime import datetime

#继承django原有数据库表
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Userprofile(AbstractUser):
    #扩展原有表
    nick_name = models.CharField(max_length=50,verbose_name =u"昵称",default="")
    birday = models.DateField(verbose_name =u"生日", null = True,blank = True)
    gender = models.CharField(choices=(("mele",u"男"),("female",u"女")),default="female",max_length=6)
    address = models.CharField(max_length=100,verbose_name =u"地址",default="")
    mobile = models.CharField(max_length=11,verbose_name =u"手机号",null = True,blank = True)
    image = models.ImageField(upload_to  = "imgage/%y/%m",default=u"image/default.png",max_length = 100,verbose_name =u"用户头像")

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class  EmailVerifyRecoed(models.Model):
    code = models.CharField(max_length = 20 , verbose_name = u'验证码')
    email = models.EmailField(verbose_name=u'邮箱地址', max_length=50)
    send_type = models.CharField(max_length = 10 ,choices=(("register",u"注册"),("forget",u"忘记")),verbose_name=u'类型')
    send_time = models.DateField(default = datetime.now,verbose_name=u"发送时间")

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code,self.email)
       

class Banner(models.Model):
    title = models.CharField(max_length = 100 , verbose_name = u'标题')
    image = models.ImageField(upload_to  = "banner/%y/%m",max_length = 100,verbose_name =u"轮播图")
    url =  models.URLField(max_length=200,verbose_name = u'访问地址')
    index = models.IntegerField(default=100,verbose_name=u"轮播顺序")
    add_time =models.DateField( default = datetime.now ,verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.title
    

