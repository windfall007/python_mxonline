#-*- encodeing:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate,login #验证方法
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password #加密密码
from django.db.models import Q #并级
from django.views.generic.base import View


from .forms import LoginForm,RegisterForm
from .models import Userprofile,EmailVerifyRecoed
from utils.email_send import send_register_email

# Create your views here.

#基础教学实例
# def user_login(request):
#     if request.method == "POST":
#         user_name = request.POST.get("username","")
#         pass_word = request.POST.get("password","")
#         user = authenticate(username = user_name,password = pass_word)
#         #验证通过返回对象，没通过返回None
#         if user is not None:
#             login(request,user)
#             #登录成功跳转首页
#             return render(request,"index.html")
#         else:
#             return render(request,"login.html",{'msg':"用户名或密码错误"})
#     elif request.method == "GET":
#         return render(request,"login.html",{})


class CustomBackend(ModelBackend):
    #自定义authenticate
    def authenticate(self,username= None, password =None ,**kwargs):
        try:
            #查询用户账号 并级查询 邮箱 手机号
            user =  Userprofile.objects.get(Q(username = username)|Q(email  = username) | Q(mobile = username))
            if user.check_password(password):
                #验证密码
                return user
        except Exception as e:
            return None

#实战基于类来作
class LoginView(View):
    def get(self,request):
        #get请求
        return render(request,"login.html",{})

    def post(self,request):
        #post请求
        login_form = LoginForm(request.POST) #实例化
        if login_form.is_valid():
            user_name = request.POST.get("username","")
            pass_word = request.POST.get("password","")
            user = authenticate(username = user_name,password = pass_word)
            #验证通过返回对象，没通过返回None
            if user is not None:
                #用户已经注册激活
                if user.is_active:
                    login(request,user) #django自带的登录
                    #登录成功跳转首页
                    return render(request,"index.html")
                else:
                    return render(request,"login.html",{'msg':"用户未激活","login_form":login_form})
            else:
                return render(request,"login.html",{'msg':"用户名或密码错误","login_form":login_form})
        else:
            return render(request,"login.html",{"login_form":login_form})


class RegisterView(View):
    def get(self,request):
        #get请求
        register_form = RegisterForm()
        return render(request,"register.html",{'register_form':register_form})
    
    def post(self,request):
        register_form = RegisterForm(request.POST) #实例化
        if register_form.is_valid():
            email_str = request.POST.get("email","")
            pass_word = request.POST.get("password","")
            user_pro = Userprofile()
            user_pro.username = email_str
            user_pro.email  = email_str
            user_pro.is_active = False #激活状态设置成未激活
            user_pro.password = make_password(pass_word) #加密密码

            user_pro.save()
            send_register_email(email_str,"register")
            
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form":register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        emailVerify =  EmailVerifyRecoed.objects.filter(code = active_code)
        if emailVerify:
            for recode in emailVerify:
                email = recode.email
                user = Userprofile.objects.get(email = email)
                user.is_active = True
                user.save()
            return render(request, "login.html")
