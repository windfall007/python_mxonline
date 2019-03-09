# -*- encodeing:utf-8 -*-
from datetime import datetime

from django.db import models

from users.models import Userprofile
from courses.models import Coures
# Create your models here.
#用户操作
class UserAsk(models.Model):
    name = models.CharField(max_length = 20,verbose_name=u"姓名")
    mobile = models.CharField(max_length=11,verbose_name=u"手机号")
    coures = models.CharField(max_length=50,verbose_name=u"课程名")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户咨询"
        verbose_name_plural = verbose_name    


class CouresComments(models.Model):
    "课程评论"
    user = models.ForeignKey(Userprofile,verbose_name = u"用户")
    coures = models.ForeignKey(Coures,verbose_name = u"课程")
    comments = models.CharField(max_length = 200,verbose_name=u"评论")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程评论"
        verbose_name_plural = verbose_name  


class UserFav(models.Model):
    "用户收藏3种里类型：课程收藏，机构收藏，教师收藏"
    user = models.ForeignKey(Userprofile,verbose_name = u"用户")
    fav_id = models.IntegerField(default=0,verbose_name=u"数据ID")
    fav_type = models.IntegerField(default=0,choices=((1,"课程"),(2,"课程机构"),(3,"教师")),verbose_name=u"收藏类型")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户收藏"
        verbose_name_plural = verbose_name  


class UserMessage(models.Model):
    #user如果def= 0 为系统消息，不等于0则是用户消息
    user = models.IntegerField(default=0,verbose_name="接受用户")
    message = models.CharField(max_length = 500,verbose_name=u"消息内容")
    has_read =models.BooleanField(default = False,verbose_name = u"是否已读")
    add_time = models.DateField(default=datetime.now, verbose_name=u"发送时间")

    class Meta:
        verbose_name = u"用户消息"
        verbose_name_plural = verbose_name  
    

class UserCoures(models.Model):
    "用户课程"
    user = models.ForeignKey(Userprofile,verbose_name = u"用户")
    coures = models.ForeignKey(Coures,verbose_name = u"课程")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户课程"
        verbose_name_plural = verbose_name      

    
