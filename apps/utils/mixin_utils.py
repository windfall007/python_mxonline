# -*- coding: utf-8 -*-
__author__ = 'bobby'

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    #修饰器 暂时不知道什么意思 可以没登录重定向登录
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


#判罚用户是否登录,收藏
def validateUserLogin(request,fav_id,fav_type):
    if request.user.is_authenticated():
        if UserFav.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type):
            return True
        else:
            return False
    else:
        return False        