# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.conf.urls import url, include

from education.dashboard.permissions.apps import get_urls as permission_url

class DashboardConfig(AppConfig):
    name = 'dashboard'

def get_urls():
    urls = [
        url(r'permission/', include(permission_url())),
    ]
    return urls
