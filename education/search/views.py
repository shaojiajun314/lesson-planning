# -*- coding: utf-8 -*-
from json import dumps
from django.http import JsonResponse
from drf_haystack.viewsets import HaystackGenericAPIView
from rest_framework.pagination import PageNumberPagination
# from .serializers import ProductIndexSerializer
from education.search.serializers import ExampleIndexSerializer

from search_indexes import ExampleIndex


class Page(PageNumberPagination):
    # 每页显示的数据条数
    max_page_size = 30
    page_size = 30
    page_size_query_param = 'size'
    # 页码
    page_query_param = 'page'

class ExampleSearchView(HaystackGenericAPIView):

    def get(self, request, *args, **kwargs):
        # type_ = request.GET.get('type', 'normal')
        qs = ExampleIndex.objects.auto_query(request.GET['value']).all()
        page = Page()
        page_data = page.paginate_queryset( \
            queryset=qs, request=request, view=self)
        data = ExampleIndexSerializer(page_data, many=True)
        # print page.get_next_link()
        # return JsonResponse([data.data, page.get_next_link()], safe=False)
        return JsonResponse({
            'msg': 'success',
            'desc': 'success',
            'code': 0,
            'data': {
                'examples': data.data,
                'next_link': page.get_next_link()
            }
        })
