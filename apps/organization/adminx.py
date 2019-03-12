#-*- encodeing:utf-8 -*-
import xadmin


from .models import CityDict,CouresOrg,Teacher

class CityDictAdmin(object):
    list_display = ['name','desc','add_time']
    search_fields = ['name','desc']
    list_filter = ['name','desc','add_time']


class CouresOrgAdmin(object):
    list_display = ['name','desc','click_num','fav_num','image','address','city','add_time']
    search_fields = ['name','desc','click_num','fav_num','image','address','city']
    list_filter =  ['name','desc','click_num','fav_num','image','address','city']


class TeacherAdmin(object):

    list_display = ['name','org','work_years','work_company','work_position','points','click_num','fav_num','add_time']
    search_fields = ['org','name','work_years','work_company','work_position','points','click_num','fav_num']
    list_filter =  ['org','name','work_years','work_company','work_position','points','click_num','fav_num']

xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CouresOrg,CouresOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)
