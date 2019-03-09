#-*- encodeing:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate,login #验证方法
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password #加密密码
from django.db.models import Q #并级查询数据
from django.views.generic.base import View
from django.http import HttpResponse


from .forms import LoginForm,RegisterForm,ForgetPwdForm,resetPwdForm
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

#用户注册
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

            if Userprofile.objects.filter(email = email_str):
                return render(request, "register.html", {"msg":"该邮箱已经被注册","register_form":register_form})

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


#用户激活
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
        else:
            return render(request, "404.html")

#忘记密码
class ForgetPwdView(View):
    def get(self, request):
        forget_passwd_form = ForgetPwdForm()
        return render(request, "forgetpwd.html",{"forget_passwd_form":forget_passwd_form})
    
    def post(self,request):
        forget_passwd_form = ForgetPwdForm(request.POST)
        if forget_passwd_form.is_valid():
            email_str = request.POST.get("email","")
            #发送验证邮件
            send_register_email(email_str,"reset")
            return HttpResponse(u"邮件已发送到您的邮箱!")
        else:
            return render(request, "forgetpwd.html", {"forget_passwd_form":forget_passwd_form})

#重置密码
class PwdResetView(View):
    def get(self, request,reset_code):
        emailVerify = EmailVerifyRecoed.objects.filter(code = reset_code)
        if emailVerify:
            for record in emailVerify:
                email = record.email
                return render(request, "password_reset.html", {"email":email})
        else:
            return render(request, "404.html")
    

class setNewPwdView(View):
    def post(self, request):
        useremail = request.POST.get("email", "")
        password = request.POST.get('password','')
        password2 = request.POST.get('password2','')
        reset_pwd_form = resetPwdForm(request.POST)
        if reset_pwd_form.is_valid():
            if password != password2:
                return render(request, "password_reset.html", {"email":useremail,"reset_pwd_form":reset_pwd_form,"msg":'密码不一致'})
           
            user = Userprofile.objects.get(email = useremail)
            user.password = make_password(password2)
            user.save()
            return render(request, "login.html")
        else:
            return render(request, "password_reset.html", {"email":useremail,"reset_pwd_form":reset_pwd_form})    
    



