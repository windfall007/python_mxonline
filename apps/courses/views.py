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
        coures =  Coures.objects.get(id = int(course_id))

        user_coures = UserCoures.objects.filter(coures = coures)
        #取所有学过这个课程的用户id
        user_ids = [ items.user.id  for items in user_coures  ] #py列表式
        #所有用户学过的课程
        all_user_coures = UserCoures.objects.filter(user_id__in = user_ids) #user_id解释：user是UserCoures的外键，可用通过_id取出user.id的值,__in可以遍历数组中的值只要有就返回出来
        #取出所有用户学过的课程id
        all_coures_ids = [ items.coures.id  for items in all_user_coures  ]
        #获取学过其他课程
        relate_courses = Coures.objects.filter(id__in=all_coures_ids).order_by("-click_nums")[:5]
        return render(request,'course-video.html',{
            'course':coures,
            'relate_courses':relate_courses,
            'tag':'info'
        })


class CourseCommentView(LoginRequiredMixin,View):
    def get(self,request,course_id):
        course =  Coures.objects.get(id = int(course_id))
        return render(request,'course-comment.html',{
            'course':course,
            'tag':'comment'
        })        
