# -*- coding: UTF-8 -*-

from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    url(r'^$', views.news_home, name='news_home'),
    url(r'^search/$', views.news_search, name='news_search'),

    url(r'^cve/$', views.cve_index, name='cve_index'),
    url(r'^cve/(?P<article_id>[0-9]+)/$', views.cve_detail, name='cve_detail'),
    url(r'^cve/search/$', views.cve_search, name='cve_search'),

    url(r'^cnnvd/$', views.cnnvd_index, name='cnnvd_index'),
    url(r'^cnnvd/(?P<article_id>[0-9]+)/$', views.cnnvd_detail, name='cnnvd_detail'),
    url(r'^cnnvd/search/$', views.cnnvd_search, name='cnnvd_search'),

    url(r'^paper/$', views.paper_index, name='paper_index'),
    url(r'^paper/(?P<article_id>[0-9]+)/$', views.paper_detail, name='paper_detail'),
    url(r'^paper/search/$', views.paper_search, name='paper_search'),

    # for intruder
    url('vulcve/$', csrf_exempt(views.ViewCVE.as_view()), name='vulcve'),
    url('vulcnnvd/$', csrf_exempt(views.ViewCNNVD.as_view()), name='vulcnnvd'),
    url('vulpaper/$', csrf_exempt(views.ViewPaper.as_view()), name='vulpaper'),
]