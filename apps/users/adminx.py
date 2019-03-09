#-*- encodeing:utf-8 -*-
import xadmin
from xadmin import views


from .models import EmailVerifyRecoed,Banner


class BaseSetting(object):
    enable_themes = True #主题功能：开启
    use_bootswatch = True


class GlobalSettings(object):
    #全局参数修改
    site_title = "慕学后台管理系统"
    site_footer = "慕学在线网"
    menu_style = "accordion"
    

class  EmailVerifyRecoedAdmin(object):
    #列表显示
    list_display = ['code','email','send_type','send_time']
    #搜索
    search_fields = ['code','email','send_type']
    #筛选
    list_filter =  ['code','email','send_type','send_time']

class BannerAdmin(object):
    #列表显示
    list_display = ['title','image','url','index','add_time']
    #搜索
    search_fields = ['title','image','url','index']
    #筛选
    list_filter = ['title','image','url','index','add_time']

xadmin.site.register(EmailVerifyRecoed,EmailVerifyRecoedAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)#注册自定义主题
xadmin.site.register(views.CommAdminView, GlobalSettings)#注册全局字段
