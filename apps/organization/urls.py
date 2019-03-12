#-*- encodeing:utf-8 -*-

from django.conf.urls import url,include

from .views import orglistView, AddUserAskView,OrgHomeView,OrgCouresView,OrgDescView,OrgTeacherView


urlpatterns = [
    url(r'^list/$', orglistView.as_view(), name="org_list"),
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
    url(r'^coures/(?P<org_id>\d+)/$', OrgCouresView.as_view(), name="org_coures"),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),
    url(r'^org_teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="org_teacher"),
        
]