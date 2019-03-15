"""mxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
import xadmin
from django.views.static import serve


from users.views import LoginView,RegisterView,ActiveUserView,ForgetPwdView,PwdResetView,setNewPwdView
from courses.views import CourseListView
from mxonline.settings import MEDIA_ROOT #上传文件夹路径


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$',TemplateView.as_view(template_name = "index.html"), name ="index"),
    url('^login/$',LoginView.as_view(), name ="login"),
    url('^register/$',RegisterView.as_view(), name ="register"),
    url(r'^active/(?P<active_code>.*)/$',ActiveUserView.as_view(),name="active"),
    url(r'^forget_password/$', ForgetPwdView.as_view(), name="forgetpwd"),
    url(r'^reset/(?P<reset_code>.*)/$', PwdResetView.as_view(), name="reset"),
    url('^setnewpwd/$',setNewPwdView.as_view(), name ="setnewpwd"),
    url(r'^captcha/', include('captcha.urls')),#验证码

    #课程机构url配置
    url(r'^org/', include('organization.urls', namespace="org")),

    #公开课
    url(r'^course/', include('courses.urls', namespace="course")),

    #用户相关操作：评论
    url(r'^operation/', include('operation.urls', namespace="operation")),

    #公开课
    url(r'^usercenter/', include('users.urls', namespace="user")),

    #配置文件上传访问的函数
    url(r'^media/(?P<path>.*)$',  serve, {"document_root":MEDIA_ROOT}),
]

