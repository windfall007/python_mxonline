#-*- encodeing:utf-8 -*-

from django.conf.urls import url,include

from .views import CourseListView,CourseDetailsView


urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name="course_list"),
    url(r'^details/(?P<course_id>.*)/$', CourseDetailsView.as_view(), name="course_details"),
]