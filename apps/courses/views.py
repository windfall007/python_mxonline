#-*- encodeing:utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View


from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Coures
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

class CourseDetailsView(View):
    def get(self,request,course_id):
        course = Coures.objects.get(id = int(course_id))
        course.click_nums += 1
        course.save()
        return render(request,"course-detail.html",{
            'course':course
        })
