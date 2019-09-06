# -*- coding: utf-8 -*-
# @CreateTime:  2017/9/21 14:20 
# @CreateBy:    Alvin
# @File:        paper.py
# @UpdateTime:
# @UpdateBy:

from __future__ import unicode_literals

import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.views.generic import View

from vulspider.models import VulPaper


# *************************
# hacker news information
# *************************
def paper_index(request):
    posts = VulPaper.objects.filter(Q(website="HackerNews") | Q(website="FreeBuf"))       # 获取全部的paper对象
    item_total = posts.count()
    paginator = Paginator(posts, 20)  # 每页显示个数
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'paper_index.html', {'item_total': item_total,
                                                'post_list': post_list})


def paper_search(request):
    if 'keywords' in request.GET:
        keyword = request.GET['keywords']
        posts = VulPaper.objects.filter(content__icontains=keyword)      # 获取全部的HackerNews对象
        item_total = posts.count()
        paginator = Paginator(posts, 20)  # 每页显示个数
        page = request.GET.get('page')
        try:
            post_list = paginator.page(page)
        except PageNotAnInteger:
            post_list = paginator.page(1)
        except EmptyPage:
            post_list = paginator.page(paginator.num_pages)
        return render(request, 'paper_search.html', {'keyword': keyword,
                                                     'item_total': item_total,
                                                     'post_list': post_list})


def paper_detail(request, article_id):
    try:
        post = VulPaper.objects.get(id=str(article_id))
        content = post.content.split('<br>')[:-2]
        if not content:
            content = [post.content]
    except VulPaper.DoesNotExist:
        raise Http404
    return render(request, 'paper_detail.html', {'post': post,
                                                 'content': content})


def paper_tem_detail(request, article_title):
    try:
        # if "【攻击预警】匿名者" in article_title:
        #     # 零时检测需要
        #     # 标题：【攻击预警】匿名者 #OpIcarus 行动公布 57 个全球银行目标，中国 10 大银行在列
        #     # 标题中出现了隔断字符导致无法正常解析到文章名
        #     post = VulPaper.objects.get(id=3239)
        # else:
        #     post = VulPaper.objects.get(title=article_title)
        post = VulPaper.objects.get(title__icontains=article_title)
        content = post.content.split('<br>')[:-2]
        if not content:
            content = [post.content]
    except:
        raise Http404
    return render(request, 'paper_detail.html', {'post': post,
                                                 'content': content})


class ViewPaper(View):

    def get(self, request):
        try:
            papers = VulPaper.objects.all()
            page_size = request.GET.get("ps", 50)
            page_num = request.GET.get("pn", 1)
            pages = Paginator(papers, page_size).page(page_num)
            data = {
                "StatusMsg": "success",
                "total": len(papers),
                "data": [{
                    "id": item.id,
                    "title": item.title,
                    "tag": item.tag,
                    "content": item.content,
                    "website": item.website,
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
                papers = VulPaper.objects.filter(
                    Q(title__icontains=keyword) |
                    Q(tag__icontains=keyword) |
                    Q(content__icontains=keyword) |
                    Q(website__icontains=keyword) |
                    Q(origin__icontains=keyword)
                )
                page_size = req.get("ps", 50)
                page_num = req.get("pn", 1)
                pages = Paginator(papers, page_size).page(page_num)
                data = {
                    "StatusMsg": "success",
                    "total": len(papers),
                    "data": [{
                        "id": item.id,
                        "title": item.title,
                        "tag": item.tag,
                        "content": item.content,
                        "website": item.website,
                        "origin": item.origin,
                        "created": item.created,
                        "updated": item.updated,
                    } for item in pages],
                }
                return JsonResponse(data=data, status=200)

            title = req.get("title")
            tag = req.get("tag")
            content = req.get("content")
            website = req.get("website")
            origin = req.get("origin")
            if action == "create":
                VulPaper.objects.create(
                    title=title,
                    tag=tag,
                    content=content,
                    website=website,
                    origin=origin,
                )
            elif action == "update":
                VulPaper.objects.filter(id=item_id).update(
                    title=title,
                    tag=tag,
                    content=content,
                    website=website,
                    origin=origin,
                )
            elif action == "delete":
                VulPaper.objects.filter(id=item_id).delete()
            else:
                raise ValueError("Invalid parameter")
            data = {
                "StatusMsg": "success"
            }
            return JsonResponse(data=data, status=200)
        except Exception as e:
            data = {"StatusMsg": str(e)}
            return JsonResponse(data=data, status=500)
