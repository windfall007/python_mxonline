from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View


from .models import CouresComments
from courses.models import Coures

from utils.mixin_utils import LoginRequiredMixin

# Create your views here.
class AddCommentView(View):
    def post(self,request):
        if request.user.is_authenticated():
            course_id = request.POST.get('course_id',0)
            comments = request.POST.get('comments','')
            
            if int(course_id) >0 and comments:
                coures_comments =CouresComments()
                course = Coures.objects.get(id = int(course_id))
                coures_comments.course = course
                coures_comments.coures_id = course_id
                coures_comments.comments = comments
                coures_comments.user = request.user
                coures_comments.save()
                return HttpResponse('{"status":"success"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')

        else:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
