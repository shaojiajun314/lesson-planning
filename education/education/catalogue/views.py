# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from json import loads

from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.views import APIView

from education.catalogue.forms import CategoryCreateForm, CategoryUpdateForm
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
        if kw.get('pk'):
            form = CategoryUpdateForm(request.POST,
                kw.get('pk'))
        else:
            form = CategoryCreateForm(request.POST,
                kw.get('parent_pk'))

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
