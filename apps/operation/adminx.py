#-*- encodeing:utf-8 -*-

import xadmin

from .models import UserAsk,CouresComments,UserFav,UserMessage,UserCoures


class UserAskAdmin(object):
    list_display = ['name','mobile','coures','add_time']
    search_fields = ['name','mobile','coures']
    list_filter =  ['name','mobile','coures','add_time']

class CouresCommentsAdmin(object):
    list_display = ['user','coures','comments','add_time']
    search_fields = ['user','coures','comments']
    list_filter =  ['user','coures','comments','add_time']


class UserFavAdmin(object):
    list_display = ['user','fav_id','fav_type','add_time']
    search_fields = ['user','fav_id','fav_type']
    list_filter =  ['user','fav_id','fav_type','add_time']


class UserMessageAdmin(object):
    list_display = ['user','message','has_read','add_time']
    search_fields = ['user','message','has_read']
    list_filter =  ['user','message','has_read','add_time']


class UserCouresAdmin(object):
    list_display = ['user','coures','add_time']
    search_fields = ['user','coures']
    list_filter =  ['user','coures','add_time']

xadmin.site.register(UserAsk,UserAskAdmin)
xadmin.site.register(CouresComments,CouresCommentsAdmin)
xadmin.site.register(UserFav,UserFavAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(UserCoures,UserCouresAdmin)
