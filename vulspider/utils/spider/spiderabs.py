# -*- coding: UTF-8 -*-

import re
import requests

CVE_KEYWORD = [r'\bjava\b', r'\btomcat\b', r'\bapache\b', r'\blinux\b', r'\bnginx\b', r'\bPHP\b', r'\bMYSQL\b',
               r'\bSSH\b', r'\bwindows\b', r'\bIIS\b', r'\bstruts2\b', r'\bsql server\b', r'\boracle\b',
               r'\belasticsearch\b', r'\bjira\b', r'\bwordpress\b', r'\brabbitmq\b', r'\bactivemq\b', r'\bdubbo\b',
               r'\bzookeeper\b', r'\bpvk\b', r'\bpostgresql\b', r'\bsql\b', r'\bhuawei\b', r'\bEthernet Switches\b']


class SpiderABS(object):

    def __init__(self, root_url):
        self.root_url = root_url

    def downloader(self, url=None):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,zh-TW;q=0.6",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
            "Upgrade-Insecure-Requests": "1"
        }
        if url:
            return requests.get(url, headers=headers, timeout=60).text
        else:
            return requests.get(self.root_url, headers=headers, timeout=60).text

    def parser(self, html):
        pass

    def collector(self, data):
        pass

    @staticmethod
    def get_middle_str(content, start, end):
        start_index = content.index(start)
        if start_index >= 0:
            start_index += len(start)
            end_index = content.index(end)
            return content[start_index: end_index]
        else:
            return ""

    @staticmethod
    def get_keyword(description):
        pat = re.compile('|'.join(CVE_KEYWORD), flags=re.IGNORECASE)
        return ';'.join(set(pat.findall(description)))

    def grab_failure(self):
        pass
