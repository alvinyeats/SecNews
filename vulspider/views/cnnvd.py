# -*- coding: utf-8 -*-
# @CreateTime:  2017/9/21 14:20 
# @CreateBy:    Alvin
# @File:        cnnvd.py
# @UpdateTime:
# @UpdateBy:

from __future__ import unicode_literals

import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.views.generic import View

from vulspider.models import VulCNNVD


# *************************
# VulCNNVD news information
# *************************
def cnnvd_index(request):
    posts = VulCNNVD.objects.all()
    item_total = posts.count()
    paginator = Paginator(posts, 20)  # 每页显示个数
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'cnnvd_index.html', {'item_total': item_total,
                                                'post_list': post_list})


def cnnvd_search(request):
    if 'keywords' in request.GET:
        keyword = request.GET['keywords']
        posts = VulCNNVD.objects.filter(
            Q(cnnvd_id__icontains=keyword) |
            Q(title__icontains=keyword) |
            Q(cve_id__icontains=keyword) |
            Q(description__icontains=keyword)
        )
        item_total = posts.count()
        paginator = Paginator(posts, 20)  # 每页显示个数
        page = request.GET.get('page')
        try:
            post_list = paginator.page(page)
        except PageNotAnInteger:
            post_list = paginator.page(1)
        except EmptyPage:
            post_list = paginator.page(paginator.num_pages)
        return render(request, 'cnnvd_search.html', {'keyword': keyword,
                                                     'item_total': item_total,
                                                     'post_list': post_list})


def cnnvd_detail(request, article_id):
    try:
        post = VulCNNVD.objects.get(id=str(article_id))
    except VulCNNVD.DoesNotExist:
        raise Http404
    return render(request, 'cnnvd_detail.html', {'post': post})


class ViewCNNVD(View):

    def get(self, request):
        try:
            cnnvds = VulCNNVD.objects.all()
            page_size = request.GET.get("ps", 50)
            page_num = request.GET.get("pn", 1)
            pages = Paginator(cnnvds, page_size).page(page_num)
            data = {
                "StatusMsg": "success",
                "total": len(cnnvds),
                "data": [{
                    "id": item.id,
                    "title": item.title,
                    "cnnvd_id": item.cnnvd_id,
                    "cve_id": item.cve_id,
                    "keyword": item.keyword,
                    "description": item.description,
                    "origin": item.origin,
                    "created": item.created,
                    "updated": item.updated,
                } for item in pages],
            }
            return JsonResponse(data=data, status=200)
        except Exception as e:
            data = {"StatusMsg": str(e)}
            return JsonResponse(data=data, status=500)

    def post(self, request):
        try:
            req = json.loads(request.body)
            item_id = req.get("id", None)
            action = req.get("action")

            if action == "search":
                keyword = req.get("keyword", None)
                cnnvds = VulCNNVD.objects.filter(
                    Q(title__icontains=keyword) |
                    Q(cnnvd_id__icontains=keyword) |
                    Q(cve_id__icontains=keyword) |
                    Q(keyword__icontains=keyword) |
                    Q(description__icontains=keyword) |
                    Q(origin__icontains=keyword)
                )
                page_size = req.get("ps", 50)
                page_num = req.get("pn", 1)
                pages = Paginator(cnnvds, page_size).page(page_num)
                data = {
                    "StatusMsg": "success",
                    "total": len(cnnvds),
                    "data": [{
                        "id": item.id,
                        "title": item.title,
                        "cnnvd_id": item.cnnvd_id,
                        "cve_id": item.cve_id,
                        "keyword": item.keyword,
                        "description": item.description,
                        "origin": item.origin,
                        "created": item.created,
                        "updated": item.updated,
                    } for item in pages],
                }
                return JsonResponse(data=data, status=200)

            title = req.get("title")
            cnnvd_id = req.get("cnnvd_id")
            cve_id = req.get("cve_id")
            keyword = req.get("keyword")
            description = req.get("description")
            origin = req.get("origin")
            if action == "create":
                VulCNNVD.objects.create(
                    title=title,
                    cnnvd_id=cnnvd_id,
                    cve_id=cve_id,
                    keyword=keyword,
                    description=description,
                    origin=origin,
                )
            elif action == "update":
                VulCNNVD.objects.filter(id=item_id).update(
                    title=title,
                    cnnvd_id=cnnvd_id,
                    cve_id=cve_id,
                    keyword=keyword,
                    description=description,
                    origin=origin,
                )
            elif action == "delete":
                VulCNNVD.objects.filter(id=item_id).delete()
            else:
                raise ValueError("Invalid parameter")
            data = {
                "StatusMsg": "success"
            }
            return JsonResponse(data=data, status=200)
        except Exception as e:
            data = {"StatusMsg": str(e)}
            return JsonResponse(data=data, status=500)
