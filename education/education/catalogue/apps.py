# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.apps import AppConfig

from education.catalogue.views import UpdateCategoryView

class CatalogueConfig(AppConfig):
    name = 'catalogue'

def get_urls():
    urls = [
        # url(r'example/(?P<pk>\d+)/update/',
        #     UpdateExampleView.as_view(),
        #     name=''),
        # url(r'example/create/',
        #     UpdateExampleView.as_view(),
        #     ),

        url(r'category/(?:(?P<parent_pk>\d+)/)?create/$',
            UpdateCategoryView.as_view(),
            ),
        url(r'category/(?P<pk>\d+)/update/$',
            UpdateCategoryView.as_view(),
            ),
    ]
    return urls
