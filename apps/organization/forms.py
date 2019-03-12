#-*- encodeing:utf-8 -*-

import re #引入正则表达式库
from django import forms
from operation.models import UserAsk

class UserAskForm(forms.ModelForm):
    class Meta:
        #根据 models 里面的的规则验证
        model = UserAsk
        #选择需要验证验证的字段
        fields = ["name","mobile","course_name"]
    
    #自定义验证字段mobile
    def clean_mobile(self):
        #clean_是固定写法，验证字段为mobile

        mobile = self.cleaned_data['mobile']

        REGEX_MOBILE = "^1[3568]\d{9}$|^147\d{8}$|^176\d{8}$"
        
        p = re.compile(REGEX_MOBILE)  #python compile() 函数将一个字符串编译为字节代码。
        if p.match(mobile):
            #验证通过
            return mobile
        else:
            return forms.ValidationError(u"手机号码非法", code="mobile_invalid") #code的字段是自定义字段


    