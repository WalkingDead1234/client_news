# -*- coding: utf-8 -*-
import scrapy
from client_news.items import ClientNewsItem
import json
from datetime import datetime, timedelta

__author__ = 'wenjie'


class NeteaseImgSpider(scrapy.Spider):
    name = "netease_img"
    allowed_domains = ["163.com"]
    start_urls = (
        "http://c.m.163.com/photo/api/list/0096/4GJ60096.json",  # 图片
    )

    last_time = datetime.now() - timedelta(minutes=30)

    def parse(self, response):
        try:
            json_list = json.loads(response.body)
            for d in json_list:
                if d['datetime'] > self.last_time.strftime("%Y-%m-%d %H:%M:%S"):
                    yield scrapy.Request("http://c.m.163.com/photo/api/set/0096/{0}.json".format(d['setid']),
                                         callback=self.parse_img, meta=d)

        except Exception, e:
            print 'shixi_wenjie1@staff.sina.com.cn',
            print '\t',
            print 'netease',
            print '\t',
            print response.url,
            print e

    def parse_img(self, response):
        try:
            d = response.meta
            item = ClientNewsItem()
            item['url'] = response.url
            item['site'] = '网易'.decode('utf-8')
            item['column'] = "图片".decode('utf-8')
            item['title'] = d.get('setname')
            item['pub_time'] = d.get('datetime')
            item['source'] = "nosource"
            item['img'] = d.get('cover')
            item['c_count'] = d.get('replynum')
            item['sum'] = d.get('desc')
            item['tag'] = "notag"
            item['content'] = json.loads(response.body)['photos'][0]["note"]
            item['create_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return item

        except Exception, e:
            print 'shixi_wenjie1@staff.sina.com.cn',
            print '\t',
            print 'netease',
            print '\t',
            print response.url,
            print e







