#-*- encodeing:utf-8 -*-

#预处理标单
from django import forms
from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    """LoginForm definition."""
    username = forms.CharField(required = True)
    password = forms.CharField(required = True , min_length = 5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required = True, min_length = 5)
    password = forms.CharField(required = True , min_length = 5)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})