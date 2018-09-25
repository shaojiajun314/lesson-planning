# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework.views import APIView

# Create your views here.

class UpdateExampleView(APIView):
    # userinfo_by_openid_form = GetUserInfoByProfileOpenidForm
    
    def get(self, request, *args, **kwargs):
        get_form = self.userinfo_by_openid_form(request.GET)

        res = {}
        if get_form.is_valid():
            res['msg']  = 'success'
            res['desc'] = 'success'
            res['code'] = 0
            res['data'] = UserInfoSerializer(get_form.user).data
        else:
            errs = loads(get_form.errors.as_json())
            desc, code = [], []
            for k, err in errs.items():
                desc.append(err[0]['message'])
                code.append(err[0]['code'])
            res['msg'] = 'fail'
            res['desc'] = desc
            res['code'] = code
        return JsonResponse(res)
