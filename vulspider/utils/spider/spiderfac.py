# -*- coding: UTF-8 -*-
import sys
from .spiderimp import CVESpider
from .spiderimp import NVDSpider
from .spiderimp import CNNVDSpider
from .spiderimp import HackerNewsSpider
from .spiderimp import FreeBufSpider
from .spiderimp import SeeBugSpider
from .spiderimp import ZeroDayCitySpider


class SimpleSpiderFactory(object):

    TARGETS = {
        "cve": "https://cassandra.cerias.purdue.edu/CVE_changes/today.html",
        "nvd": "https://nvd.nist.gov/",
        "cnnvd": "http://www.cnnvd.org.cn/web/vulnerability/queryLds.tag?pageno=1",
        "hackernews": "http://hackernews.cc/archives/category/今日推送",
        "freebuf": "http://www.freebuf.com/vuls",
        "seebug": "https://www.seebug.org/rss/new/",
        "zerodaycity": "https://0day.city/feed",
    }

    def create_spider(self, spider_type):
        spider_store = {
            "cve": CVESpider(self.TARGETS[spider_type]),
            "nvd": NVDSpider(self.TARGETS[spider_type]),
            "cnnvd": CNNVDSpider(self.TARGETS[spider_type]),
            "hackernews": HackerNewsSpider(self.TARGETS[spider_type]),
            "freebuf": FreeBufSpider(self.TARGETS[spider_type]),
            "seebug": SeeBugSpider(self.TARGETS[spider_type]),
            "zerodaycity": ZeroDayCitySpider(self.TARGETS[spider_type]),
        }
        return spider_store[spider_type]

    def order_spider(self, spider_type):
        spider = self.create_spider(spider_type)
        sys.stdout.write("[+] Spider <{spider_type}> Object was created, ready to download target page...\n".format(spider_type=spider_type))
        html = spider.downloader()
        sys.stdout.write("[+] Target page was download, ready to parse html...\n")
        data = spider.parser(html)
        sys.stdout.write("[+] Start collect data...\n")
        spider.collector(data)


