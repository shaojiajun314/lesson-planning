# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.conf.urls import url

# apps
from education.search.views import ExampleSearchView

class SearchConfig(AppConfig):
    name = 'search'


def get_urls():
    urls = [
        url(r'example/',
            ExampleSearchView.as_view(),
            name='search-example'),
    ]
    return urls
