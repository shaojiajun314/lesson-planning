# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

#rest
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

#lib
from education.lib.permissions import IsStaff
from education.lib.baseviews import BaseApiView

#apps
from education.dashboard.permissions.forms import (UserPermissonCreateForm,
    UserPermissonDeleteForm)


User = get_user_model()

class Page(PageNumberPagination):
    # 每页显示的数据条数
    max_page_size = 30
    page_size = 30
    page_size_query_param = 'size'
    # 页码
    page_query_param = 'page'

from education.catalogue.models import (Category, Example, EDUFile)
from django.contrib.contenttypes.models import ContentType
from education.education_user.serializers import UserBaseInfoSerializer

class UserPermissonListView(APIView):
    type_maps = {
        'modify_category': (Category, 'modify_category'),
        'modify_example': (Example, 'modify_example'),
        'modify_edufile': (EDUFile, 'modify_edufile'),
        # 'modify_courseware': (ContentType.objects.get_for_model(CourseWare),
        #     'modify_courseware'),
    }

    permission_classes = [IsStaff]

    def get(self, request, *arg, **kw):
        res = {
            'msg': 'success',
            'desc': 'success',
            'code': 0,
        }
        type = request.GET['type']
        model_type, codename = self.type_maps[type]
        # modify_category, modify_example
        permission = Permission.objects.get(codename=codename,
            content_type=ContentType.objects.get_for_model(model_type))
        user_qs = User.objects.filter(user_permissions=permission)
        # XXX: 分页
        # page = Page()
        # page_data = page.paginate_queryset( \
        #     queryset=user_qs, request=request, view=self)

        data = UserBaseInfoSerializer(user_qs, many=True)
        # res['data'] = {'users': data.data,
        #     'next_link': page.get_next_link()}
        res['data'] = data.data
        return JsonResponse(res, safe=False)

class UserPermissonUpdateView(BaseApiView):
    permission_classes = [IsStaff]

    def post(self, request, *args, **kw):
        if kw.get('username'):
            form = UserPermissonDeleteForm(request.data,
                kw.get('username'))
        else:
            form = UserPermissonCreateForm(request.data)

        if form.is_valid():
            res = {
                'msg': 'success',
                'desc': 'success',
                'code': 0,
            }
            form.save()
        else:
            res = self.err_response(form)
        return JsonResponse(res)
