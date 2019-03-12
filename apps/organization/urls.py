#-*- encodeing:utf-8 -*-

from django.conf.urls import url,include

from .views import orglistView, AddUserAskView,OrgHomeView


urlpatterns = [
    url(r'^list/$', orglistView.as_view(), name="org_list"),
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),#正则取纯数字
]