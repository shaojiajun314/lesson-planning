# -*- coding: utf-8 -*-
#python
from __future__ import unicode_literals
from json import loads

#django
from django.shortcuts import render
from django.http import JsonResponse

#rest
from rest_framework.views import APIView

#apps
from education.catalogue.models import Category
from education.catalogue.serializers import CategorySerializer
from education.catalogue.forms import (CategoryCreateForm, CategoryUpdateForm,
    ExampleCreateForm, ExampleUpdateForm)
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

################################################################################
#                              分类                                            #
################################################################################

# 分类创建及更新
class UpdateCategoryView(BaseApiView):
    def post(self, request, *args, **kw):
        if kw.get('pk'):
            form = CategoryUpdateForm(request.POST,
                kw.get('pk'))
        else:
            form = CategoryCreateForm(request.POST,
                kw.get('parent_pk'))

        if form.is_valid():
            res = {
                'msg': 'success',
                'desc': 'success',
                'code': 0,
            }

            form.save()
            # res['data'] = UserInfoSerializer(form.user).data
        else:
            res = self.err_response(form)
        return JsonResponse(res)

#获取分类列表
class CategoryView(APIView):
    def get(self, request, *arg, **kw):
        parent_pk = kw.get('parent_pk')
        res = {
            'msg': 'success',
            'desc': 'success',
            'code': 0,
        }
        if not parent_pk:
            print dir(Category)
            tree = Category.get_root_nodes()
            print tree
            data = CategorySerializer(tree, many=True)
            res['data'] = data.data
            return JsonResponse(res, safe=False)
            # return HttpResponse(JSONRenderer().render(tree))
        try:
            node = Category.objects.get(id=parent_pk)
            data = CategorySerializer(node.get_children(), many=True)
        except Category.DoesNotExist:
            return JsonResponse({'msg':'invaild id',
                'desc': '该分类不存在'}, status=404)
        else:
            res['data'] = data.data
            return JsonResponse(res, safe=False)


################################################################################
#                              题目                                            #
################################################################################

# 题目创建及更新
class UpdateExampleView(BaseApiView):
    def post(self, request, *args, **kw):
        # images = request.FILES.get("file", None)
        if kw.get('pk'):
            form = ExampleUpdateForm(request.POST,
                kw.get('pk'))
        else:
            form = ExampleCreateForm(request.POST)
        if form.is_valid():
            res = {
                'msg': 'success',
                'desc': 'success',
                'code': 0,
            }
            form.save()
            # res['data'] = UserInfoSerializer(form.user).data
        else:
            res = self.err_response(form)
        return JsonResponse(res)

# 题目分类更新
class UpdateExampleCategoryView(BaseApiView):
    def post(self, request, *args, **kw):
        pass
