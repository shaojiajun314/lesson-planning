# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.apps import AppConfig

from education.catalogue.views import UpdateExampleView

class CatalogueConfig(AppConfig):
    name = 'catalogue'

def get_urls():
    urls = [
        url(r'example/(?P<pk>\d+)/update/',
            UpdateExampleView.as_view(),
            name=''),
        url(r'example/create/',
            UpdateExampleView.as_view(),
            ),
    ]
    return urls
