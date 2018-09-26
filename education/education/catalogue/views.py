# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework.views import APIView

from education.catalogue.forms import CategoryCreateForm
# Create your views here.

class BaseApiView(APIView):
    def err_response(self, form):
        res = {}
        errs = loads(form.errors.as_json())
        desc, code = [], []
        for k, err in errs.items():
            desc.append(err[0]['message'])
            code.append(err[0]['code'])
        res['msg'] = 'fail'
        res['desc'] = desc
        res['code'] = code
        return res

class UpdateCategoryView(BaseApiView):
    def post(self, request, *args, **kw):
        # images = request.FILES.get("file", None)
        form = self.CategoryCreateForm(request.POST,
            kw.get('parent_pk'),
            kw.get('pk'))

        if form.is_valid():
            res = {}
            res['msg']  = 'success'
            res['desc'] = 'success'
            res['code'] = 0

            form.save()
            # res['data'] = UserInfoSerializer(form.user).data
        else:
            res = self.err_response(form)

        return JsonResponse(res)
