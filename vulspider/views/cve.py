# -*- coding: utf-8 -*-
# @CreateTime:  2017/9/21 14:20 
# @CreateBy:    Alvin
# @File:        cve.py
# @UpdateTime:
# @UpdateBy:
import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.views.generic import View

from vulspider.models import VulCVE


# *************************
# VulCVE news information
# *************************
def cve_index(request):
    posts = VulCVE.objects.all()       # 获取全部的NVD对象
    item_total = posts.count()
    paginator = Paginator(posts, 20)  # 每页显示个数
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'cve_index.html', {'item_total': item_total,
                                              'post_list': post_list})


def cve_search(request):
    if 'keywords' in request.GET:
        keyword = request.GET['keywords']
        posts = VulCVE.objects.filter(Q(cve_id__icontains=keyword) | Q(description__icontains=keyword))      # 获取全部的NVD对象
        item_total = posts.count()
        paginator = Paginator(posts, 20)  # 每页显示个数
        page = request.GET.get('page')
        try:
            post_list = paginator.page(page)
        except PageNotAnInteger:
            post_list = paginator.page(1)
        except EmptyPage:
            post_list = paginator.page(paginator.num_pages)
        return render(request, 'cve_search.html', {'keyword': keyword,
                                                   'item_total': item_total,
                                                   'post_list': post_list})


def cve_detail(request, article_id):
    try:
        post = VulCVE.objects.get(id=str(article_id))
    except VulCVE.DoesNotExist:
        raise Http404
    return render(request, 'cve_detail.html', {'post': post})


class ViewCVE(View):

    def get(self, request):
        try:
            cves = VulCVE.objects.all()
            page_size = request.GET.get("ps", 50)
            page_num = request.GET.get("pn", 1)
            pages = Paginator(cves, page_size).page(page_num)
            data = {
                "StatusMsg": "success",
                "total": len(cves),
                "data": [{
                    "id": item.id,
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
                cves = VulCVE.objects.filter(
                    Q(cve_id__icontains=keyword) |
                    Q(keyword__icontains=keyword) |
                    Q(description__icontains=keyword) |
                    Q(origin__icontains=keyword)
                )
                page_size = req.get("ps", 50)
                page_num = req.get("pn", 1)
                pages = Paginator(cves, page_size).page(page_num)
                data = {
                    "StatusMsg": "success",
                    "total": len(cves),
                    "data": [{
                        "id": item.id,
                        "cve_id": item.cve_id,
                        "keyword": item.keyword,
                        "description": item.description,
                        "origin": item.origin,
                        "created": item.created,
                        "updated": item.updated,
                    } for item in pages],
                }
                return JsonResponse(data=data, status=200)

            cve_id = req.get("cve_id")
            keyword = req.get("keyword")
            description = req.get("description")
            origin = req.get("origin")
            if action == "create":
                VulCVE.objects.create(
                    cve_id=cve_id,
                    keyword=keyword,
                    description=description,
                    origin=origin,
                )
            elif action == "update":
                VulCVE.objects.filter(id=item_id).update(
                    cve_id=cve_id,
                    keyword=keyword,
                    description=description,
                    origin=origin,
                )
            elif action == "delete":
                VulCVE.objects.filter(id=item_id).delete()
            else:
                raise ValueError("Invalid parameter")
            data = {
                "StatusMsg": "success"
            }
            return JsonResponse(data=data, status=200)
        except Exception as e:
            data = {"StatusMsg": str(e)}
            return JsonResponse(data=data, status=500)
