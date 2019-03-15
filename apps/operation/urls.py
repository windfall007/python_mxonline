#-*- encodeing:utf-8 -*-

from django.conf.urls import url,include

from .views import AddCommentView


urlpatterns = [
    url(r'^add_comment/$', AddCommentView.as_view(), name="operation_add_comment"),
]