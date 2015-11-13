#! /usr/bin/env python
#coding=utf-8
__author__ = '帅'

import scrapy
from client_news.items import ClientNewsItem
import traceback
import time
import datetime
import re
import json

class IfengSpider(scrapy.Spider):
    name = "fenghuang_photo"
    allowed_domains = ["ifeng.com"]
    start_urls = (
                "http://api.iclient.ifeng.com/get_pic_list?gv=4.6.5&av=0&proid=ifengnews" \
                "&os=ios_9.1&vt=5&screen=750x1334&publishid=4002&uid=086f4de209f0d590a7931bba7584dd5ae8c40064",
    )
    time = time.time()
    last_time = time - 3600

    def parse(self, response):
        try:
            body = response.body
            body_json = json.loads(body)
            item_list = body_json.get("body").get("item")
            #print "type: ",item_list,type(item_list)
            for item0 in item_list:
                    url = item0.get('links')[0].get('url')
                    #print "url: ",url
                    img_src = item0.get('thumbnail')
                    title = item0.get("title")
                    comments = item0.get("comments")
                    column = "图片".decode("utf-8")
                    pub_time = item0.get("updateTime")
                    timearray = time.strptime(pub_time, "%Y-%m-%d %H:%M:%S")
                    timestamp = int(time.mktime(timearray))
                    if timestamp > self.last_time:
                        yield scrapy.Request(url, callback=self.parse_img,meta={'title':title,
                            'img':img_src,'column':column,'comments':comments,'pub_time':pub_time})
        except Exception, e:
            print 'shixi_zhangshuai@staff.sina.com.cn',
            print '\t',
            print 'fenghuang',
            print '\t',
            print response.url,
            print e

    def parse_img(self,response):
        item = ClientNewsItem()
        now = datetime.datetime.now()
        create_time = now.strftime('%Y-%m-%d %H:%M:%S')
        item['create_time'] = create_time

        body = response.body
        body_json = json.loads(body)
        slides_list = body_json.get("body").get("slides")
        source = body_json.get("body").get("source")
        #print "source: ",source,type(slides_list)
        content = ''
        img = ''
        for item1 in slides_list:
            content += item1.get("description")
        #print "content: ",content
        try:
            item['url'] = response.url
            item['site'] = '凤凰'.decode('utf-8')
            item['source'] = source
            item['title'] = response.meta['title']
            item['column'] = response.meta['column']
            item['c_count'] = response.meta['comments']
            item['pub_time'] = response.meta['pub_time']
            item['img'] = response.meta['img']
            item['content'] = content
            item['tag'] = "notag"
            item['sum'] = "无摘要".decode("utf-8")
            return item

        except Exception, e:
            print 'shixi_zhangshuai@staff.sina.com.cn',
            print '\t',
            print 'fenghuang',
            print '\t',
            print response.url,
            print e

