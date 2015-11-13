# -*- coding: utf-8 -*-
__author__ = 'xiutx'
import scrapy
from client_news.items import ClientNewsItem
import traceback
import time
import re
import json

class NeteaseSpider(scrapy.Spider):
    name = "netease"
    allowed_domains = ["163.com"]
    start_urls = (
        "http://c.m.163.com/nc/article/headline/T1348647909107/0-140.html",    # 要闻
        "http://c.m.163.com/nc/article/list/T1348649079062/0-60.html",         # 体育
        "http://c.m.163.com/nc/article/list/T1348648517839/0-60.html",         # 娱乐
        "http://c.m.163.com/nc/article/list/T1348648756099/0-60.html",         # 财经
        "http://c.m.163.com/nc/article/list/T1348648141035/0-20.html",         # 军事
        "http://c.m.163.com/nc/article/list/T1348649580692/0-26.html"          # 科技
    )

    time = time.time()
    last_time = time - 3600

    def parse(self, response):
        try:
            body = response.body
            body_json = json.loads(body)

            key = re.findall(r'T[0-9]{13}', response.url)
            json_list = body_json.get(key[0])
            tname = json_list[0]['tname']
            for newitem in json_list:

                ptime = newitem.get("ptime")
                url = newitem.get("url_3w")

                if url:
                    timearray = time.strptime(ptime, "%Y-%m-%d %H:%M:%S")
                    timestamp = int(time.mktime(timearray))
                    if timestamp > self.last_time:
                        yield scrapy.Request(url, callback=self.parse_page, meta={'json': newitem, 'column': tname})

        except Exception, e:
            print 'shixi_tianxiang@staff.sina.com.cn', #此处替换为自己的邮箱
            print '\t',
            print 'netease',
            print '\t',
            print response.url,
            print e

    def parse_page(self, response):
        item = ClientNewsItem()

        import datetime
        now = datetime.datetime.now()
        create_time = now.strftime('%Y-%m-%d %H:%M:%S')
        item['create_time'] = create_time

        try:
            content = response.xpath('//div[@id="endText"]/p[not(style)]//text()').extract()
            if not content:
                content = response.xpath('//div[@class="entext"]//text()').extract()

            tag = response.meta['json'].get("TAGS")
            if not tag:
                tag ='notag'

            item['url'] = response.url
            item['site'] = '网易'.decode('utf-8')
            item['column'] = response.meta['column']
            item['title'] = response.meta['json'].get("title")
            item['pub_time'] = response.meta['json'].get("ptime")
            item['source'] = response.meta['json'].get("source")
            item['img'] = response.meta['json'].get("imgsrc")
            item['c_count'] = response.meta['json'].get("replyCount")
            item['sum'] = response.meta['json'].get("digest")
            item['tag'] = tag
            item['content'] = content

            return item

        except Exception, e:
            print 'shixi_tianxiang@staff.sina.com.cn', #此处替换为自己的邮箱
            print '\t',
            print 'netease',
            print '\t',
            print response.url,
            print e
