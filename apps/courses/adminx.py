#-*- encodeing:utf-8 -*-
import xadmin

from .models import Coures,Lesson,Video,CouresRes


class CouresAdmin(object):
    list_display = ['cover','name','desc','detail','degree','degree','learn_times','students','fav_num','click_nums','add_time']
    search_fields = ['cover','name','desc','detail','degree','degree','learn_times','students','fav_num','click_nums']
    list_filter =  ['cover','name','desc','detail','degree','degree','learn_times','students','fav_num','click_nums','add_time']


class LessonAdmin(object):
    list_display = ['coures','name','add_time']
    search_fields = ['coures','name']
    list_filter = ['coures__name','name','add_time']


class VideoAdmin(object):
    list_display = ['lesson','name','add_time']
    search_fields = ['lesson','name']
    list_filter = ['lesson','name','add_time']


class CouresResAdmin(object):
    list_display = ['coures','name','download','add_time']
    search_fields = ['coures','name','download']
    list_filter =  ['coures','name','download','add_time']

xadmin.site.register(Coures,CouresAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CouresRes,CouresResAdmin)
