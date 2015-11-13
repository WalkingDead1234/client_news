# -*- coding: utf-8 -*-

import scrapy
import json
import codecs
import sys
from pprint import pprint
from client_news.items import ClientNewsItem
import time

__author__ = 'xiutx'

class BaiduSpider(scrapy.Spider):
    name = "baidu"
    allowed_domains = ["baidu.com"]

    def start_requests(self):

        params = {'from': 'app', 'display_time': '0',
            'os': 'iphone', 'cuid': '6e8fe3bb2eb9276b03925870e08df124a993fb2d', 'action': '1'}

        # 要闻
        base_url = "http://api.baiyue.baidu.com/sn/api/newchosenlist"
        request_list = [scrapy.FormRequest(base_url, formdata=params, callback=self.parse_list, meta={"column": "要闻"}) ]

        # 体育，娱乐，财经，军事，科技
        d = {}
        base_url = "http://api.baiyue.baidu.com/sn/api/recommendlist"
        params = {
            'mid': 'qunidaye',
            'ts': '0',
        }

        columns = {"体育", "娱乐", "财经", "军事", "科技"}
        for column in columns:
            params['topic'] = column
            d[column] = params.copy()
        request_list.extend([scrapy.FormRequest(base_url, formdata=data, callback=self.parse_list, meta={"column": column})
                             for (column, data) in d.items()])

        return request_list

    def parse_list(self, response):
        meta = response.meta
        d = json.loads(response.body)
        last_time = time.time() - 3600
        last_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - 30 * 60))
        if meta['column'] == "要闻":
            if d.has_key('data') and d['data'].has_key('news'):
                for index in range(len(d['data']['news'])):
                    item = ClientNewsItem()
                    news = d['data']['news'][index]
                    item['site'] = "百度"
                    item['url'] =  news['url']
                    item['column'] = "要闻"
                    item['title'] = news['title']
                    item['pub_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(news['sourcets'][:-3])))
                    if item['pub_time'] < last_time_str:
                        continue
                    item['source'] = news['site']
                    whole_content = news['content']
                    content = ""
                    for i in range(len(whole_content)):
                        if type(whole_content[i]['data']) == dict:
                            if not item.get('img'):
                                for value in whole_content[i]['data'].values():
                                    if type(value) == dict and value.get('small'):
                                        item['img'] = value['small']['url']
                                    elif type(value) == dict and value.get('url'):
                                        item['img'] = value['url']
                                    elif type(value) == dict and value.get('big'):
                                        item['img'] = value['big']
                            continue
                        content += whole_content[i]['data']
                    item['content'] = content
                    item['sum'] = news['abs']

                    item['tag'] = "no tag"
                    item['c_count'] = 0
                    from datetime import datetime
                    item['create_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if not item.get('img'):
                        item['img'] = "no image"
                    yield item
        else:
            if d.has_key('data') and d['data'].has_key('news'):
                for index in range(len(d['data']['news'])):
                    item = ClientNewsItem()
                    news = d['data']['news'][14]
                    item['site'] = "百度"
                    item['url'] =  news['url']
                    item['column'] = meta['column']
                    item['title'] = news['title']
                    item['pub_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(news['sourcets'][:-3])))
                    if item['pub_time'] < last_time_str:
                        continue
                    item['source'] = news['site']
                    whole_content = news['content']
                    content = ""
                    for i in range(len(whole_content)):
                        if type(whole_content[i]['data']) == dict:
                            item['img'] = whole_content[i]['data'].values()[0]['url']
                            continue
                        content += whole_content[i]['data']
                    item.get('img')
                    item['content'] = content
                    item['sum'] = news['abs']
                    item['tag'] = "no tag"
                    item['c_count'] = 0
                    from datetime import datetime
                    item['create_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if not item.get('img'):
                        item['img'] = "no image"
                    yield item

