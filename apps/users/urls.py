#-*- encodeing:utf-8 -*-

from django.conf.urls import url,include

from .views import UserCenterInfoView,UserCenterMycourseView,UserCenterMessageView,UserCenterFavView


urlpatterns = [
    url(r'^info/$', UserCenterInfoView.as_view(), name="usercenter_info"),
    url(r'^mycourse/$', UserCenterMycourseView.as_view(), name="usercenter_mycourse"),
    url(r'^fav/$', UserCenterFavView.as_view(), name="usercenter_fav"),
    url(r'^message/$', UserCenterMessageView.as_view(), name="usercenter_message"),
]