#-*- encodeing:utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View


from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Coures
from operation.models import UserFav,UserCoures

from utils.mixin_utils import LoginRequiredMixin
# Create your views here.

class CourseListView(View):
    def get(self,request):
        all_courses = Coures.objects.all().order_by("-add_time") #时间排序
        
        hot_courses = Coures.objects.all().order_by("-click_nums")[:3]

        sort =  request.GET.get('sort','')
        if sort == 'hot':
            all_courses = Coures.objects.all().order_by("-click_nums") #根据点击数排序

        if sort == 'students':
            all_courses = Coures.objects.all().order_by("-students") #根据学生数排序
        
        #对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)

        courses = p.page(page)
        return render(request,"course-list.html",{
            'all_courses':courses,
            "sort":sort,
            'hot_courses':hot_courses
        })


#判罚用户是否登录
def validateUserLogin(request,fav_id,fav_type):
    if request.user.is_authenticated():
        print(request.user,fav_id,fav_type)
        if UserFav.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type):
            return True
        else:
            return False
    else:
        return False

class CourseDetailsView(View):
    def get(self,request,course_id):
        course = Coures.objects.get(id = int(course_id))
        #增加课程点击数
        course.click_nums += 1
        course.save()

        tag = course.tag
        if tag:
            #根据课程标签筛选出相关课程推荐
            relate_coures = Coures.objects.filter(tag = tag)[:1]
        else:
            relate_coures = []
        
        #收藏课程
        has_fav_course = validateUserLogin(request,course.id,1)
        
        #收藏机构
        has_fav_org = validateUserLogin(request,course.coures_org.id,2)
        
        return render(request,"course-detail.html",{
            'course':course,
            'relate_coures':relate_coures,
            'has_fav_org':has_fav_org,
            'has_fav_course':has_fav_course
        })


#继承修饰器， 没登录跳转到登录， 顺序 从左到右
class CourseInfoView(LoginRequiredMixin,View):
    def get(self,request,course_id):
        course =  Coures.objects.get(id = int(course_id))
        course.students += 1
        course.save()

        return render(request,'course-video.html',{
            'course':course
        })
