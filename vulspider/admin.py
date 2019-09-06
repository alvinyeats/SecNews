# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from vulspider.models import VulCVE
from vulspider.models import VulCNNVD
from vulspider.models import VulPaper


class VulCVEAdmin(admin.ModelAdmin):
    list_display = ('cve_id', 'keyword', 'created', 'updated',)
    search_fields = ('cve_id', 'keyword', 'description',)
    list_filter = ('keyword',)


class VulCNNVDAdmin(admin.ModelAdmin):
    list_display = ('cnnvd_id', 'cve_id', 'keyword', 'created', 'updated',)
    search_fields = ('cnnvd_id', 'cve_id', 'keyword', 'description',)
    list_filter = ('keyword',)


class VulPaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'website', 'created', 'updated',)
    search_fields = ('title', 'website', 'content',)
    list_filter = ('website',)


admin.site.register(VulCVE, VulCVEAdmin)
admin.site.register(VulCNNVD, VulCNNVDAdmin)
admin.site.register(VulPaper, VulPaperAdmin)
