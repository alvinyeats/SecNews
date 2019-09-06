# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import re
import sys
from urllib.parse import urlparse
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import feedparser

from .spiderabs import SpiderABS
from vulspider.models import VulCVE
from vulspider.models import VulCNNVD
from vulspider.models import VulPaper


class CVESpider(SpiderABS):
    def __init__(self, root_url):
        SpiderABS.__init__(self, root_url)
        self.name = "CVE"

    def parser(self, html):
        data = []
        if not html:
            return data
        today_cve = self.get_middle_str(html, "New entries:", "Graduations")
        cve_soup = BeautifulSoup(today_cve, "lxml")
        for a in cve_soup.find_all('a'):
            origin = a["href"]
            sub_html = self.downloader(origin)
            sub_cve_soup = BeautifulSoup(sub_html, "lxml")
            cve_id = sub_cve_soup.find(nowrap="nowrap").find("h2").get_text()
            table = sub_cve_soup.find("div", id="GeneratedTable").find("table")
            description = table.find_all("tr")[3].find("td").get_text().strip()
            keyword = self.get_keyword(description)
            created = datetime.strptime(table.find_all("tr")[10].find("b").get_text(), "%Y%m%d")
            data.append({
                "cve_id": cve_id,
                "description": description,
                "keyword": keyword,
                "created": created,
                "origin": origin,
            })
        return data

    def collector(self, data):
        for item in data:
            sys.stdout.write(" [-] {target}, ready to create\n".format(target=item["cve_id"]))
            try:
                VulCVE.objects.create(
                    cve_id=item["cve_id"],
                    description=item["description"],
                    keyword=item["keyword"],
                    created=item["created"],
                    origin=item["origin"],
                )
                sys.stdout.write("     Create success\n")
            except :
                sys.stdout.write("     Already Exist\n")


class NVDSpider(SpiderABS):
    def __init__(self, root_url):
        SpiderABS.__init__(self, root_url)
        self.name = "NVD"

    def parser(self, html):
        data = []
        if not html:
            return data
        nvd_soup = BeautifulSoup(html, "lxml")
        for li in nvd_soup.find('ul', id='latestVulns').find_all('li'):
            origin = self.root_url + li.find('a')['href'][1:]
            sub_html = self.downloader(origin)
            sub_nvd_soup = BeautifulSoup(sub_html, 'lxml')
            div = sub_nvd_soup.find('div', class_='bs-callout bs-callout-info')
            cve_id = div.find('a').get_text().strip()
            created = datetime.strptime(div.find('span').get_text().strip(), "%m/%d/%Y")
            description = sub_nvd_soup.find('p', {'data-testid': 'vuln-description'}).get_text().strip()
            keyword = self.get_keyword(description)
            data.append({
                "cve_id": cve_id,
                "description": description,
                "keyword": keyword,
                "created": created,
                "origin": origin,
            })
        return data

    def collector(self, data):
        for item in data:
            sys.stdout.write(" [-] {target}, ready to create\n".format(target=item["cve_id"]))
            try:
                VulCVE.objects.create(
                    cve_id=item["cve_id"],
                    description=item["description"],
                    keyword=item["keyword"],
                    created=item["created"],
                    origin=item["origin"],
                )
                sys.stdout.write("     Create success\n")
            except:
                sys.stdout.write("     Already Exist\n")


class CNNVDSpider(SpiderABS):
    def __init__(self, root_url):
        SpiderABS.__init__(self, root_url)
        self.name = "CNNVD"

    def parser(self, html):
        data = []
        if not html:
            return data
        soup = BeautifulSoup(html, "lxml")
        for tag in soup.find_all("a", class_="a_title2"):
            origin = urlparse.urljoin(self.root_url, tag['href'])
            sub_html = self.downloader(origin)
            sub_soup = BeautifulSoup(sub_html, 'lxml')
            detail = sub_soup.find('div', class_='detail_xq w770')
            title = detail.find('h2').get_text().strip()
            lis = detail.find_all('li')
            cnnvd_id = lis[0].get_text().strip()[8:]
            cve_id = lis[2].find_all('a')[-1].get_text().strip()
            description = sub_soup.find('div', class_='d_ldjj').get_text().strip()
            keyword = self.get_keyword(description)
            created = lis[6].find_all('a')[-1].get_text().strip()
            data.append({
                "title": title,
                "cnnvd_id": cnnvd_id,
                "cve_id": cve_id,
                "description": description,
                "keyword": keyword,
                "created": created,
                "origin": origin,
            })
        return data

    def collector(self, data):
        for item in data:
            sys.stdout.write(" [-] {target}, ready to create\n".format(target=item["cnnvd_id"]))
            try:
                VulCNNVD.objects.create(
                    title=item["title"],
                    cnnvd_id=item["cnnvd_id"],
                    cve_id=item["cve_id"],
                    description=item["description"],
                    keyword=item["keyword"],
                    created=item["created"],
                    origin=item["origin"],
                )
                sys.stdout.write("     Create success\n")
            except:
                sys.stdout.write("     Already Exist\n")


class HackerNewsSpider(SpiderABS):
    def __init__(self, root_url):
        SpiderABS.__init__(self, root_url)
        self.name = "HackerNews"

    def parser(self, html):
        data = []
        if not html:
            return data
        soup = BeautifulSoup(html, "lxml")
        for post in soup.find_all('article', id='article'):
            title = post.find('div', class_='classic-list-left').a['title']
            origin = post.find('div', class_='classic-list-left').a['href']
            a_parts = post.find('div', class_='light-post-meta').find_all('a')
            created = datetime.strptime(a_parts[1].get_text(), "%Y-%m-%d")
            tag = a_parts[3].get_text()
            sub_html = self.downloader(origin)
            sub_soup = BeautifulSoup(sub_html, "lxml")
            p_parts = sub_soup.find('div', class_='post-body clearfix').find_all('p')
            content = ""
            for p in p_parts:
                content += p.get_text()
                if p.get_text():
                    content += "<br>"
            data.append({
                "title": title,
                "tag": tag,
                "content": content,
                "website": "HackerNews",
                "created": created,
                "origin": origin,
            })
        return data

    def collector(self, data):
        for item in data:
            sys.stdout.write(" [-] {target}, ready to create\n".format(target=item["title"]))
            try:
                VulPaper.objects.create(
                    title=item["title"],
                    tag=item["tag"],
                    content=item["content"],
                    website=item["website"],
                    created=item["created"],
                    origin=item["origin"],
                )
                sys.stdout.write("     Create success\n")
            except:
                sys.stdout.write("     Already Exist\n")


class FreeBufSpider(SpiderABS):
    def __init__(self, root_url):
        SpiderABS.__init__(self, root_url)
        self.name = "FreeBuf"    
        
    def downloader(self, url=None):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,zh-TW;q=0.6",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/66.0.3359.181 Safari/537.36",
            "Upgrade-Insecure-Requests": "1",
        }
        if url:
            return requests.get(url, headers=headers, timeout=60).content
        else:
            return requests.get(self.root_url, headers=headers, timeout=60).content

    def parser(self, html):
        data = []
        if not html:
            return data
        soup = BeautifulSoup(html, "lxml")
        for post in soup.find_all('div', class_="news_inner news-list"):
            news_info = post.find('div', class_="news-info")
            title = news_info.find_all('a')[0].get_text().strip()
            tag = news_info.find('span', class_="tags").get_text().strip()
            origin = news_info.find_all('a')[0]['href']
            created = news_info.find('span', class_="time").get_text().strip()
            sub_html = self.downloader(origin)
            sub_soup = BeautifulSoup(sub_html, "lxml")
            p_parts = sub_soup.find('div', id='contenttxt').find_all('p')
            content = ""
            for p in p_parts:
                content += p.get_text()
                if p.get_text():
                    content += "<br>"
            data.append({
                "title": title,
                "tag": tag,
                "content": content,
                "website": self.name,
                "created": created,
                "origin": origin,
            })
        return data

    def collector(self, data):
        for item in data:
            sys.stdout.write(" [-] {target}, ready to create\n".format(target=item["title"]))
            try:
                VulPaper.objects.create(
                    title=item["title"],
                    tag=item["tag"],
                    content=item["content"],
                    website=item["website"],
                    created=item["created"],
                    origin=item["origin"],
                )
                sys.stdout.write("     Create success\n")
            except:
                sys.stdout.write("     Already Exist\n")


class SeeBugSpider(SpiderABS):
    def __init__(self, root_url):
        SpiderABS.__init__(self, root_url)
        self.name = "SeeBug"      

    def downloader(self, url=None):
        return feedparser.parse(self.root_url)

    def parser(self, html):
        data = []
        if not html:
            return data
        items = html.entries
        for item in items:
            data.append({
                "title": item.title,
                "tag": item.category,
                "content": item.description,
                "website": self.name,
                "created": datetime.strptime(item.updated_date[:10], "%Y-%m-%d"),
                "origin": item.link,
            })
        return data

    def collector(self, data):
        for item in data:
            sys.stdout.write(" [-] {target}, ready to create\n".format(target=item["title"]))
            try:
                VulPaper.objects.create(
                    title=item["title"],
                    tag=item["tag"],
                    content=item["content"],
                    website=item["website"],
                    created=item["created"],
                    origin=item["origin"],
                )
                sys.stdout.write("     Create success\n")
            except:
                sys.stdout.write("     Already Exist\n")


class ZeroDayCitySpider(SpiderABS):
    def __init__(self, root_url):
        SpiderABS.__init__(self, root_url)
        self.name = "ZeroDayCity"

    def downloader(self, url=None):
        return feedparser.parse(self.root_url)

    def parser(self, html):
        data = []
        if not html:
            return data
        items = html.entries
        for item in items:
            # if have cve id, save in cve model
            if re.findall(r"CVE-\d+-\d+", item.title):
                data.append({
                    "cve_id": re.findall(r"CVE-\d+-\d+", item.title)[0],
                    "description": item.title,
                    "keyword": self.get_keyword(item.title),
                    "created": datetime.strptime(item.published, "%a, %d %b %Y %H:%M:%S +0000"),
                    "origin": item.link,
                })
            # else save in vulpaper hackernews model
            else:
                sys.stdout.write(" [-] {target}, ready to create\n".format(target=item["title"]))
                try:
                    VulPaper.objects.create(
                        title=item.title,
                        tag="0day",
                        content=item.description,
                        website="HackerNews",
                        created=datetime.strptime(item.published, "%a, %d %b %Y %H:%M:%S +0000"),
                        origin=item.link,
                    )
                    sys.stdout.write("     Create success\n")
                except:
                    sys.stdout.write("     Already Exist\n")
        return data

    def collector(self, data):
        for item in data:
            sys.stdout.write(" [-] {target}, ready to create\n".format(target=item["cve_id"]))
            try:
                VulCVE.objects.create(
                    cve_id=item["cve_id"],
                    description=item["description"],
                    keyword=item["keyword"],
                    created=item["created"],
                    origin=item["origin"],
                )
                sys.stdout.write("     Create success\n")
            except:
                sys.stdout.write("     Already Exist\n")
