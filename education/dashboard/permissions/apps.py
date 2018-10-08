# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.apps import AppConfig

from education.dashboard.permissions.views import UserPermissonListView, UserPermissonUpdateView

class PermissionsConfig(AppConfig):
    name = 'permissions'

def get_urls():
    urls = [
        url(r'users/query/$',
            UserPermissonListView.as_view(),
        ),
        url(r'users/create/$',
            UserPermissonUpdateView.as_view(),
        ),
        url(r'users/(?P<username>[\w-]{1,33})/delete/$',
            UserPermissonUpdateView.as_view(),
        ),
    ]
    return urls
