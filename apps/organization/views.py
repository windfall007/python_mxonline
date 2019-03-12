#-*- encodeing:utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger #分页插件


from .models import CouresOrg,CityDict
from .forms import UserAskForm

# Create your views here.
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

        #查询外键的数据
        all_courses = coures_org.coures_set.all()[:3]
        all_teachers =  coures_org.teacher_set.all()[:1]

        return render(request, "org-detail-homepage.html",{
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'coures_org':coures_org,
            'activate_page':'a'
        })

#机构课程
class OrgCouresView(View):
    def get(self,request,org_id):
        #查询外键的值
        coures_org = CouresOrg.objects.get(id=int(org_id))
        all_courses = coures_org.coures_set.all()

        return render(request,"org-detail-course.html",{
            'coures_org':coures_org,
            'all_courses':all_courses,
            'activate_page':'b'
        })

#机构介绍
class OrgDescView(View):
    def get(self,request,org_id):
        coures_org = CouresOrg.objects.get(id=int(org_id))

        return render(request,"org-detail-desc.html",{
            'coures_org':coures_org,
            'activate_page':'c'
        })        

#机构讲师
class OrgTeacherView(View):
    def get(self,request,org_id):
        coures_org = CouresOrg.objects.get(id=int(org_id))
        #查询外键的值
        all_teachers =  coures_org.teacher_set.all()

        return render(request,"org-detail-teachers.html",{
            'coures_org':coures_org,
            'all_teachers':all_teachers,
            'activate_page':'d'
        })       
    
