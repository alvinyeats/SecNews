# -*- coding: utf-8 -*-
from traceback import format_exc
from django.core.management.base import BaseCommand, CommandError
from vulspider.utils import SimpleSpiderFactory, spider_error


class Command(BaseCommand):
    help = 'Crawl security information from different website!'

    def add_arguments(self, parser):
        parser.add_argument(
            '-c',
            type=str,
            help='Set the website',
        )

    def handle(self, *args, **options):
        site = options['c']
        if not site:
            raise CommandError(
                "please select target from (cve/nvd/cnnvd/hackernews/freebuf/seebug) \n" +
                "Usage: python manage.py -c target")
        try:
            simple_spider = SimpleSpiderFactory()
            simple_spider.order_spider(site)
        except AttributeError:
            spider_error(site, format_exc())
            raise CommandError("craw target site failed")

