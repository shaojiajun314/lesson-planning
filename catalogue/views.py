# -*- coding: utf-8 -*-
#python
from __future__ import unicode_literals

#django
from django.http import JsonResponse

#rest
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

#lib
from education.lib.baseviews import BaseApiView

#apps
from education.catalogue.models import Category, Example
from education.catalogue.serializers import CategorySerializer, ExampleSerializer
from education.catalogue.forms import (CategoryCreateForm, CategoryUpdateForm,
    ExampleCreateForm, ExampleUpdateForm)
# Create your views here.
################################################################################
#                              分页                                            #
################################################################################

class Page(PageNumberPagination):
    # 每页显示的数据条数
    max_page_size = 30
    page_size = 1
    page_size_query_param = 'size'
    # 页码
    page_query_param = 'page'

################################################################################
#                              分类                                            #
################################################################################

# 分类创建及更新
class UpdateCategoryView(BaseApiView):
    def post(self, request, *args, **kw):
        if kw.get('pk'):
            form = CategoryUpdateForm(request.data,
                request.FILES,
                kw.get('pk'))
        else:
            form = CategoryCreateForm(request.data,
                request.FILES,
                kw.get('parent_pk'))

        if form.is_valid():
            res = {
                'msg': 'success',
                'desc': 'success',
                'code': 0,
            }

            model = form.save()
            res['data'] = {'id': model.id}
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
            tree = Category.get_root_nodes()
            data = CategorySerializer(tree, many=True)
            res['data'] = data.data
            return JsonResponse(res, safe=False)
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
        if kw.get('pk'):
            form = ExampleUpdateForm(request.data,
                kw.get('pk'))
        else:
            form = ExampleCreateForm(request.data,
                request.FILES,)
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

# 获取题目列表
class ExampleView(BaseApiView):
    def get(self, request, *args, **kw):
        res = {
            'msg': 'success',
            'desc': 'success',
            'code': 0,
        }
        category_pk = kw.get('category_pk')
        if category_pk:
            manager = Category.objects.get(id=category_pk).examples
        else:
            manager = Example.objects

        # 用于之后过滤数据 暂时没用
        example_qs = manager.all()
        page = Page()
        page_data = page.paginate_queryset( \
            queryset=example_qs, request=request, view=self)
        data = ExampleSerializer(page_data, many=True)
        res['data'] = {'examples': data.data,
            'next_link': page.get_next_link()}
        return JsonResponse(res, safe=False)
