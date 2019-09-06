# -*- coding: utf-8 -*-
# @CreateTime:  2017/9/21 14:10 
# @CreateBy:    Alvin
# @File:        home.py
# @UpdateTime:
# @UpdateBy:

from __future__ import unicode_literals

from django.shortcuts import render
from django.db.models import Q

from vulspider.models import VulCVE
from vulspider.models import VulCNNVD
from vulspider.models import VulPaper


# Create your views here.
def news_home(request):
    cve_list = VulCVE.objects.all()[:10]
    cnnvd_list = VulCNNVD.objects.all()[:10]
    paper_list = VulPaper.objects.filter(Q(website="HackerNews")|Q(website="FreeBuf"))[:10]
    return render(request,
                  'news_home.html',
                  {'cve_list': cve_list,
                   'cnnvd_list': cnnvd_list,
                   'paper_list': paper_list})


def news_search(request):
    if 'keywords' in request.GET:
        keyword = request.GET['keywords']
        nvd_list = VulCVE.objects.filter(Q(cve_id__icontains=keyword) | Q(description__icontains=keyword))
        cnnvd_list = VulCNNVD.objects.filter(
            Q(cnnvd_id__icontains=keyword) |
            Q(title__icontains=keyword) |
            Q(cve_id__icontains=keyword) |
            Q(description__icontains=keyword)
        )
        paper_list = VulPaper.objects.filter(content__icontains=keyword)
        return render(request,
                      'news_home.html',
                      {'nvd_list': nvd_list[:10] if len(nvd_list) > 10 else nvd_list,
                       'cnnvd_list': cnnvd_list[:10] if len(cnnvd_list) > 10 else cnnvd_list,
                       'paper_list': paper_list[:10] if len(paper_list) > 10 else paper_list})

