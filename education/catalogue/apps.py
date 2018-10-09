# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.apps import AppConfig

from education.catalogue.views import (UpdateCategoryView, CategoryView,
    UpdateExampleView, ExampleView, DocxView, AncestorsCategoryView,
    ExampleDetaiView, UpdateFilesView, FileView)

class CatalogueConfig(AppConfig):
    name = 'catalogue'

def get_urls():
    urls = [
        # 分类
        url(r'category/(?:(?P<parent_pk>\d+)/)?create/$',
            UpdateCategoryView.as_view(),
        ),
        url(r'category/(?P<pk>\d+)/update/$',
            UpdateCategoryView.as_view(),
        ),
        url(r'category/(?:(?P<parent_pk>\d+)/)?query/$',
            CategoryView.as_view(),
        ),
        url(r'category/(?P<category_pk>\d+)/ancestors/query/$',
            AncestorsCategoryView.as_view(),
        ),

        # 题目
        url(r'example/create/$',
            UpdateExampleView.as_view(),
        ),
        url(r'example/(?P<pk>\d+)/update/$',
            UpdateExampleView.as_view(),
        ),
        url(r'example/(?P<pk>\d+)/query/$',
            ExampleDetaiView.as_view(),
        ),
        url(r'category/(?:(?P<category_pk>\d+)/)?examples/query/$',
            ExampleView.as_view(),
        ),

        url(r'examples/docx/create/$',
            DocxView.as_view(),
        ),

        # 课件　提纲
        url(r'file/(?:(?P<pk>\d+)/)?(?P<type>[\w-]{1,20})/create/$',
            UpdateFilesView.as_view(),
        ),
        url(r'category/(?:(?P<category_pk>\d+)/)?(?P<type>[\w-]{1,20})/files/query/$',
            FileView.as_view(),
        ),



    ]
    return urls
