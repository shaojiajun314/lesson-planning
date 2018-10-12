# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class CustomerConfig(AppConfig):
    name = 'customer'



from django.conf.urls import url

from education.dashboard.customer.views import APILikeSearch
def get_urls():
    urls = [
        url(r'customer-like/query/$',
            APILikeSearch.as_view(),
        ),
    ]
    return urls
