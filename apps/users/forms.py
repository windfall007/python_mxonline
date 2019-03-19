#-*- encodeing:utf-8 -*-

#预处理标单
from django import forms
from captcha.fields import CaptchaField
from .models import Userprofile


class LoginForm(forms.Form):
    """LoginForm definition."""
    username = forms.CharField(required = True)
    password = forms.CharField(required = True , min_length = 5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required = True, min_length = 5)
    password = forms.CharField(required = True , min_length = 5)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required = True, min_length = 5)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})

class resetPwdForm(forms.Form):
    password = forms.CharField(required = True , min_length = 5)
    password2 = forms.CharField(required = True , min_length = 5)
    
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ['nick_name', 'gender', 'birday', 'address', 'mobile']



class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ['image']


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)
        
