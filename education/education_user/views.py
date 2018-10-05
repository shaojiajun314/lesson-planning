# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.contrib.auth import login as auth_login

#lib
from education.lib.baseviews import BaseApiView

#apps
from education.education_user.forms import LoginForm, UserCreateForm
from education.education_user.serializers import UserInfoSerializer
# Create your views here.


class APILogInView(BaseApiView):
    def post(self, request, *arg, **kw):
        if request.user.is_authenticated():
            return JsonResponse({
                'msg':  'Login success',
                'desc': '已登录',
                'code': 0,
                'data': UserInfoSerializer(request.user).data
            })
        form = LoginForm(request.data)
        if form.is_valid():
            auth_login(request, form.user)
            res = {
                'msg': 'Login success',
                'desc': '登录成功',
                'code': 0,
            }
            res['data'] = UserInfoSerializer(request.user).data
        else:
            res = self.err_response(form)
        return JsonResponse(res)


class APIRegisterView(BaseApiView):
    def post(self, request, *args, **kwargs):
        # request.session.setdefault('user',{})
        form = UserCreateForm(request.data)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            res = {
                'msg': 'Register success',
                'desc': '注册成功',
                'code': 0,
            }
            res['data'] = UserInfoSerializer(request.user).data
        else:
            res = self.err_response(form)
        return JsonResponse(res)
