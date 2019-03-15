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
    tag = models.CharField(max_length=10, blank=True, null=True, verbose_name=u"课程标签")
    youneed_know = models.CharField(default="", max_length=300, verbose_name=u"课程须知")
    teacher_tell = models.CharField(default="", max_length=300, verbose_name=u"老师告诉你")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return self.name

    def get_lesson_num(self):
        #通过外键lesson获取它的数量_set是Django自带的
        return self.lesson_set.all().count()

    #short_description设置后可在adminX显示该字段
    get_lesson_num.short_description = "章节数"

    def get_learn_users(self):
        #学习用户
        #获取usercoures的models的长度5
        return self.usercoures_set.all()[:5]

    def get_course_lesson(self):
        #所有课程的章节
        return self.lesson_set.all()
    
    def get_coures_res(self):
        return self.couresres_set.all()

    def get_course_comment(self):
        #获取课程评论
        return self.courescomments_set.all().order_by("-id")


#章节表设计
class Lesson(models.Model):
    coures = models.ForeignKey(Coures, verbose_name=u"课程")
    name = models.CharField(max_length=50, verbose_name=u"章节名")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程章节"
        verbose_name_plural = verbose_name        

    def get_lesson_video(self):
        return self.video_set.all()

    def __str__(self):
        return self.name

#视频表设计
class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name = u"章节")
    name = models.CharField(max_length=50, verbose_name=u"视频名称")
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")
    url = models.CharField(max_length=200, default="", verbose_name=u"访问地址")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频列表"
        verbose_name_plural = verbose_name    
    
    def __str__(self):
        return self.name

#课程资源
class CouresRes(models.Model):
    coures = models.ForeignKey(Coures, verbose_name=u"课程")
    name = models.CharField(max_length=50, verbose_name=u"名称")
    download=  models.FileField(upload_to="coures/resource/%y/%m",verbose_name=u"资源文件",max_length = 100)
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name