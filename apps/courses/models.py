# -*- encodeing:utf-8 -*-
from django.db import models
from datetime import datetime

from organization.models import CouresOrg,Teacher
# Create your models here.

# 课程表设计
class Coures(models.Model):
    coures_org = models.ForeignKey(CouresOrg, verbose_name=u"机构名称",null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    detail = models.TextField(verbose_name=u"课程详情")
    degree = models.CharField(choices=(
        ("cj", u"初级"), ("zj", u"中级"), ("gj", u"高级")), max_length=2, verbose_name=u"课程难度")
    teacher = models.ForeignKey(Teacher, verbose_name=u"讲师", null=True, blank=True)
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长（分钟）")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_num = models.IntegerField(default=0, verbose_name=u"收藏人数")
    cover = models.ImageField(upload_to="coures/%y/%m", verbose_name=u"课程封面")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return self.name

#章节表设计
class Lesson(models.Model):
    coures = models.ForeignKey(Coures, verbose_name=u"课程")
    name = models.CharField(max_length=50, verbose_name=u"章节名")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程章节"
        verbose_name_plural = verbose_name        

    def __str__(self):
        return self.name
    

#视频表设计
class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name = u"章节")
    name = models.CharField(max_length=50, verbose_name=u"视频名称")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频列表"
        verbose_name_plural = verbose_name    


#课程资源
class CouresRes(models.Model):
    coures = models.ForeignKey(Coures, verbose_name=u"课程")
    name = models.CharField(max_length=50, verbose_name=u"名称")
    download=  models.FileField(upload_to="coures/resource/%y/%m",verbose_name=u"资源文件",max_length = 100)
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name