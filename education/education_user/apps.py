# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.apps import AppConfig

from education.education_user.views import (APILogInView, APIRegisterView)

class EducationUserConfig(AppConfig):
    name = 'education_user'

def get_urls():
    urls = [
        url(r'login/$',
            APILogInView.as_view(),
        ),
        url(r'register/$',
            APIRegisterView.as_view(),
        ),

    ]
    return urls
