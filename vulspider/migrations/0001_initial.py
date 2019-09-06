# -*- coding: utf-8 -*-

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VulCNNVD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='\u6f0f\u6d1e\u540d\u79f0')),
                ('cnnvd_id', models.CharField(max_length=20, unique=True, verbose_name='CNNVD\u7f16\u53f7')),
                ('cve_id', models.CharField(max_length=20, unique=True, verbose_name='CVE\u7f16\u53f7')),
                ('description', models.TextField(verbose_name='\u6f0f\u6d1e\u63cf\u8ff0')),
                ('keyword', models.CharField(default='', max_length=100, verbose_name='\u5173\u952e\u5b57')),
                ('created', models.DateField(verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated', models.DateField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('origin', models.URLField(verbose_name='\u6e90\u5730\u5740')),
            ],
            options={
                'ordering': ['-updated'],
                'verbose_name': 'CNNVD',
                'verbose_name_plural': 'CNNVD',
            },
        ),
        migrations.CreateModel(
            name='VulCVE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cve_id', models.CharField(max_length=20, unique=True, verbose_name='CVE\u7f16\u53f7')),
                ('description', models.TextField(verbose_name='\u6f0f\u6d1e\u63cf\u8ff0')),
                ('keyword', models.CharField(default='', max_length=100, verbose_name='\u5173\u952e\u5b57')),
                ('created', models.DateField(verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated', models.DateField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('origin', models.URLField(verbose_name='\u6e90\u5730\u5740')),
            ],
            options={
                'ordering': ['-updated'],
                'verbose_name': 'CVE',
                'verbose_name_plural': 'CVE',
            },
        ),
        migrations.CreateModel(
            name='VulPaper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='\u6807\u9898')),
                ('tag', models.CharField(default='', max_length=100, verbose_name='\u6807\u7b7e')),
                ('content', models.TextField(verbose_name='\u5185\u5bb9')),
                ('website', models.CharField(max_length=20, verbose_name='\u7ad9\u70b9\u540d\u79f0')),
                ('created', models.DateField(verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated', models.DateField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('origin', models.URLField(verbose_name='\u6e90\u5730\u5740')),
            ],
            options={
                'ordering': ['-updated'],
                'verbose_name': 'Paper',
                'verbose_name_plural': 'Paper',
            },
        ),
    ]
