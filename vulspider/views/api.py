# -*- coding: utf-8 -*-
# @CreateTime:  2017/11/8 19:28 
# @CreateBy:    Alvin
# @File:        api.py
# @UpdateTime:
# @UpdateBy:

from __future__ import unicode_literals

from datetime import datetime
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework import mixins

from vulspider.models import VulCVE
from vulspider.models import VulPaper

TODAY = datetime.now()


# --------------------------CVE api data set------------------------- #
class CVEItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VulCVE
        fields = ('id', 'cve_id', 'description')


class CVEViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = VulCVE.objects.filter(updated=TODAY).exclude(keyword__isnull=True).exclude(keyword__exact='')
    serializer_class = CVEItemSerializer


# --------------------------HackerNews api data set------------------------- #
class HNItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VulPaper
        fields = ('id', 'title', 'origin')


class HNViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = VulPaper.objects.filter(website="HackerNews", updated=TODAY)
    serializer_class = HNItemSerializer


# --------------------------SeeBug api data set------------------------- #
class SBItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VulPaper
        fields = ('title', 'origin')


class SBViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = VulPaper.objects.filter(website="SeeBug", updated=TODAY)
    serializer_class = SBItemSerializer


# -------------------------FreeBuf api data set------------------------- #
class FBItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VulPaper
        fields = ('title', 'origin')


class FBViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = VulPaper.objects.filter(website="FreeBuf", updated=TODAY)
    serializer_class = FBItemSerializer


# ----------------------------Aliyun api data set------------------------- #
class AYItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VulPaper
        fields = ('title', 'origin')


class AYViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = VulPaper.objects.filter(website="ALiYun", updated=TODAY)
    serializer_class = AYItemSerializer

