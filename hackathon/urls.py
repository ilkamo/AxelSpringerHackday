"""hackathon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from . import views
from views  import CategoryView, RelatedView, DifferentView, CompletedtView, RecommendView
# from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^category/(?P<category>\w+)/$', CategoryView.as_view(), name='category'),
    url(r'^more/(?P<article_id>\w+)/$', RelatedView.as_view(), name='related'),
    url(r'^skip/(?P<article_id>\w+)/$', DifferentView.as_view(), name='different'),
    url(r'^completed/(?P<article_id>\w+)/$', CompletedtView.as_view(), name='completed'),
    url(r'^recommendations/$', RecommendView.as_view(), name='recommend'),
]