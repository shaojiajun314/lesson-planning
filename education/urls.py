"""education URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.views.static import serve
from django.conf.urls import url, include

from education.index_views import IndexRedirctView
from education.catalogue.apps import get_urls as catalogue_urls
from education.education_user.apps import get_urls as user_urls
from education.dashboard.apps import get_urls as dashboard_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', IndexRedirctView.as_view()),
    url(r'^api/catalogue/', include(catalogue_urls())),
    url(r'^api/user/', include(user_urls())),
    url(r'^api/dashboard/', include(dashboard_urls())),

    url(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
]
