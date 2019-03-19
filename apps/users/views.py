#-*- encodeing:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout #验证方法
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password #加密密码
from django.db.models import Q #并级查询数据
from django.views.generic.base import View
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse


from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from .forms import LoginForm,RegisterForm,ForgetPwdForm,resetPwdForm,UserInfoForm,UploadImageForm,ModifyPwdForm
from .models import Userprofile,EmailVerifyRecoed,Banner
from operation.models import UserCoures,UserFav,UserMessage
from organization.models import CouresOrg
from courses.models import Teacher,Coures
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin

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
                    return HttpResponseRedirect(reverse("index"))
                    # return render(request,"index.html")
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

#个人资料
class UserCenterInfoView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'usercenter-info.html')

    def post(self, request):
        #instance 可以直接让在其方法上保存
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')   


    
#我的课程
class UserCenterMycourseView(LoginRequiredMixin,View):
    def get(self,request):
        coures = UserCoures.objects.filter(user = request.user)
        return render(request,'usercenter-mycourse.html',{
            'coures':coures
        })


#我的收藏
class UserCenterFavView(LoginRequiredMixin,View):
    def get(self,request):
        type = int(request.GET.get('type',0))
        if type > 3 or type < 1:
            type = 1

        
        def dataList(el):
            list = []
            data =  UserFav.objects.filter(fav_type= type,user = request.user)
            for i in data:
                row = el.objects.get(id = int(i.fav_id))
                list.append(row)
            return list
        
        #1"课程",2"课程机构",3"教师"
        listdata = []
        if type == 1:
           listdata = dataList(Coures)

        if type == 2:
           listdata = dataList(CouresOrg)

        if type == 3:
           listdata = dataList(Teacher)           

        return render(request,'usercenter-fav.html',{
            'list':listdata,
            'type':type
        })

#我的消息
class UserCenterMessageView(LoginRequiredMixin,View):
    def get(self,request):
        all_messages = UserMessage.objects.filter(user = request.user.id)
        #用户进入个人消息后清空未读消息的记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_messages in all_unread_messages:
            unread_messages.has_read = True
            unread_messages.save()

        #对个人消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 5, request=request)

        messages = p.page(page)

        return render(request,'usercenter-message.html',{
            "messages":messages
        })


class UploadImageView(LoginRequiredMixin, View):
    """
    用户修改头像
    """
    def post(self, request):
        #文件格式需要加上request.FILES
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')




class UpdatePwdView(LoginRequiredMixin, View):
    """ 修改密码 """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')

    
class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """
    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        send_register_email(email, "update_email")

        return HttpResponse('{"status":"success"}', content_type='application/json')


class LogoutView(View):
    """用户登出 """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class IndexView(View):
    #慕学在线网 首页
    def get(self, request):
        #取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        courses = Coures.objects.filter(is_banner=False)[:6]
        banner_courses = Coures.objects.filter(is_banner=True)[:3]
        course_orgs = CouresOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners':all_banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'course_orgs':course_orgs
        })        