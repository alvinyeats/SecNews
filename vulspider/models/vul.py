# -*- coding: UTF-8 -*-

from django.db import models


class VulCVE(models.Model):
    cve_id = models.CharField("CVE编号", max_length=20, unique=True)
    description = models.TextField("漏洞描述")
    keyword = models.CharField("关键字", max_length=100, default="")
    created = models.DateField("创建时间")
    updated = models.DateField("更新时间", auto_now=True)
    origin = models.URLField("源地址")

    def __unicode__(self):
        return self.cve_id

    class Meta:
        verbose_name = 'CVE'
        verbose_name_plural = 'CVE'
        ordering = ['-updated']


class VulCNNVD(models.Model):
    title = models.CharField("漏洞名称", max_length=200)
    cnnvd_id = models.CharField("CNNVD编号", max_length=20, unique=True)
    cve_id = models.CharField("CVE编号", max_length=20, unique=True)
    description = models.TextField("漏洞描述")
    keyword = models.CharField("关键字", max_length=100, default="")
    created = models.DateField("创建时间")
    updated = models.DateField("更新时间", auto_now=True)
    origin = models.URLField("源地址")

    def __unicode__(self):
        return self.cve_id

    class Meta:
        verbose_name = 'CNNVD'
        verbose_name_plural = 'CNNVD'
        ordering = ['-updated']


class VulPaper(models.Model):
    title = models.CharField("标题", max_length=200, unique=True)
    tag = models.CharField("标签", max_length=100, default="")
    content = models.TextField("内容")
    website = models.CharField("站点名称", max_length=20)
    created = models.DateField("创建时间")
    updated = models.DateField("更新时间", auto_now=True)
    origin = models.URLField("源地址")

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'Paper'
        verbose_name_plural = 'Paper'
        ordering = ['-updated']
