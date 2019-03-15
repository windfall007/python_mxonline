#-*- encodeing:utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger #分页插件

from .models import CouresOrg,CityDict
from courses.models import Coures,Teacher
from operation.models import UserFav
from .forms import UserAskForm

# Create your views here.

#判罚用户是否登录
def validateUserLogin(request,fav_id,fav_type):
    if request.user.is_authenticated():
        if UserFav.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type):
            return True
        else:
            return False
    else:
        return False

class orglistView(View):
    def get(self,request):
        #查询数据库
        org_list = CouresOrg.objects.all()
        all_city = CityDict.objects.all()
        cityid = request.GET.get('city','')
        category = request.GET.get('ct','')

        hot_org = org_list.order_by('-click_num')[:3]

        #筛选
        if cityid:
           org_list =  org_list.filter(city_id = int(cityid))

        if category:
            org_list = org_list.filter(category= category)

        sort = request.GET.get('sort','')
        if sort == 'students':
            org_list = org_list.order_by('-students')
        elif sort == 'courses':
            org_list = org_list.order_by('-course_num')

        #统计数量
        total = org_list.count()

        #对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(org_list, 2, request=request)

        orgs = p.page(page)

        return render(request,'org-list.html',
            {'org_list':orgs,
            'all_city':all_city,
            'total':total,
            'cityid':cityid,
            'category':category,
            'hot_org':hot_org,
            'sort':sort
        })


class AddUserAskView(View):
    def post(self,request):
        #将提交的数据直接在form验证表单
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            #如果不填commit = True  数据库不会保存值
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')

#机构首页
class OrgHomeView(View):
    def get(self,request,org_id):
        coures_org = CouresOrg.objects.get(id=int(org_id))
        coures_org.click_num +=1
        coures_org.save()
        has_fav = validateUserLogin(request,coures_org.id,2)
        #查询外键的数据
        all_courses = coures_org.coures_set.all()[:3]
        all_teachers =  coures_org.teacher_set.all()[:1]

        return render(request, "org-detail-homepage.html",{
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'coures_org':coures_org,
            'activate_page':'a',
            'has_fav':has_fav
        })

#机构课程
class OrgCouresView(View):
    def get(self,request,org_id):
        #查询外键的值
        coures_org = CouresOrg.objects.get(id=int(org_id))
        all_courses = coures_org.coures_set.all()
        has_fav = validateUserLogin(request,coures_org.id,2)


        #对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 2, request=request)

        courses = p.page(page)

        return render(request,"org-detail-course.html",{
            'coures_org':coures_org,
            'all_courses':courses,
            'activate_page':'b',
            'has_fav':has_fav
        })

#机构介绍
class OrgDescView(View):
    def get(self,request,org_id):
        coures_org = CouresOrg.objects.get(id=int(org_id))
        has_fav = validateUserLogin(request,coures_org.id,2)
        return render(request,"org-detail-desc.html",{
            'coures_org':coures_org,
            'activate_page':'c',
            'has_fav':has_fav
        })        

#机构讲师
class OrgTeacherView(View):
    def get(self,request,org_id):
        coures_org = CouresOrg.objects.get(id=int(org_id))
        #查询外键的值
        all_teachers =  coures_org.teacher_set.all()
        has_fav = validateUserLogin(request,coures_org.id,2)

        return render(request,"org-detail-teachers.html",{
            'coures_org':coures_org,
            'all_teachers':all_teachers,
            'activate_page':'d',
            'has_fav':has_fav
        })       
    

#用户收藏
class AddUserFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        def removeData(obj):
            data = obj.objects.get(id=int(fav_id))
            data.fav_num -= 1
            if data.fav_num < 0:
                data.fav_num = 0
            data.save()

        def addData(obj):
            data = obj.objects.get(id=int(fav_id))
            data.fav_num +=1
            data.save()

        if not request.user.is_authenticated():
            #判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        else:
            exist_records = UserFav.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
            if exist_records:
                #收藏已经存在
                exist_records.delete()

                if int(fav_type) == 1:
                    #课程收藏减1
                    removeData(Coures)

                if int(fav_type) == 2:
                    removeData(CouresOrg)
                 
                if int(fav_type) == 3:
                    removeData(Teacher)   

                return HttpResponse('{"status":"success", "msg":"取消收藏"}', content_type='application/json')

            else:
                #未收藏 
                user_fav =  UserFav() #实例化
                if int(fav_id) > 0 and (int(fav_type) > 0 and int(fav_type) < 4):
                    user_fav.user = request.user
                    user_fav.fav_id = int(fav_id)
                    user_fav.fav_type = int(fav_type)
                    user_fav.save()

                    if int(fav_type) == 1:
                        addData(Coures)

                    if int(fav_type) == 2:
                        addData(CouresOrg)

                    if int(fav_type) == 3:
                        addData(Teacher)

                    return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')

                else:

                    return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')
    

#课程列表
class TeacherListView(View):
    def get(self,request):
        all_teacher =  Teacher.objects.all()
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_teacher =  all_teacher.order_by('-click_num')
        else:
            sort = ''

        tj_teacher = all_teacher.order_by('-fav_num')[:5]

        #分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teacher, 2, request=request)

        teachers = p.page(page)        
        return render(request,'teachers-list.html',{
            'teachers':teachers,
            'sort':sort,
            'tj_teacher':tj_teacher
        })


class TeacherDetailsView(View):
    def get(self,request,teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_num += 1
        teacher.save()

        all_coures_list =  Coures.objects.filter(teacher =teacher,coures_org = teacher.org)


        tj_teacher =Teacher.objects.filter(org = teacher.org).order_by("-click_num")[:3]

        return render(request,'teacher-detail.html',{
            'teacher':teacher,
            'coures_list':all_coures_list,
            'tj_teacher':tj_teacher
        })
