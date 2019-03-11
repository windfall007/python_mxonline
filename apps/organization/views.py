#-*- encodeing:utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View


from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from .models import CouresOrg,CityDict
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