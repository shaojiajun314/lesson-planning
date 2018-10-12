# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# django
from django.http import JsonResponse
from django.contrib.auth import get_user_model

#lib
from education.lib.permissions import IsStaff

# rest
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

#apps
from education.education_user.serializers import UserBaseInfoSerializer

User = get_user_model()
################################################################################
#                              分页                                            #
################################################################################

class Page(PageNumberPagination):
    # 每页显示的数据条数
    max_page_size = 30
    page_size = 30
    page_size_query_param = 'size'
    # 页码
    page_query_param = 'page'


################################################################################
#                              查询                                            #
################################################################################
class APILikeSearch(APIView):
    permission_classes = [IsStaff]
    def get(self, request, *arg, **kw):
        like_username = request.GET.get('like_username')
        if like_username:
            users = User.objects.filter(username__contains=like_username.strip())
        else:
            users = User.objects.all()
        page = Page()
        page_data = page.paginate_queryset( \
            queryset=users, request=request, view=self)
        data = UserBaseInfoSerializer(page_data, many=True)
        return JsonResponse({
            'msg':  'success',
            'desc': '获取成功',
            'code': 0,
            'data'  :   {
                'users_list'        :   data.data,
                'next_link'         :   page.get_next_link()
            },
        })
