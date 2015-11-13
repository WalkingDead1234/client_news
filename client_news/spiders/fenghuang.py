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

class FenghuangSpider(scrapy.Spider):
    name = "fenghuang"
    allowed_domains = ["ifeng.com"]
    start_urls = (
        "http://api.iclient.ifeng.com/ClientNews?id=SYLB10,SYDT10,SYRECOMMEND&page=%d&gv=4.4.5" \
        "&av=4.4.5&uid=862095023463703&deviceid=862095023463703&proid=ifengnews&os=android_19" \
        "&df=androidphone&vt=5&screen=1152x1920&publishid=9023",  #头条
        "http://api.iclient.ifeng.com/ClientNews?id=TY43,FOCUSTY43&page=%d&gv=4.4.5&av=4.4.5" \
              "&uid=862095023463703&deviceid=862095023463703&proid=ifengnews&os=android_19" \
              "&df=androidphone&vt=5&screen=1152x1920&publishid=9023",         #体育
        "http://api.iclient.ifeng.com/ClientNews?id=CJ33,FOCUSCJ33&page=%d&gv=4.4.5&av=4.4.5" \
                  "&uid=862326025768413&deviceid=862326025768413&proid=ifengnews&os=android_16" \
                  "&df=androidphone&vt=5&screen=540x960&publishid=9023",         #财经
        "http://api.iclient.ifeng.com/ClientNews?id=YL53,FOCUSYL53&gv=4.6.5" \
        "&av=0&proid=ifengnews&os=ios_9.1&vt=5&screen=750x1334&publishid=4002" \
        "&uid=086f4de209f0d590a7931bba7584dd5ae8c40064",         #娱乐
        "http://api.iclient.ifeng.com/ClientNews?id=KJ123,FOCUSKJ123&gv=4.6.5" \
        "&av=0&proid=ifengnews&os=ios_9.1&vt=5&screen=750x1334&publishid=4002" \
        "&uid=086f4de209f0d590a7931bba7584dd5ae8c40064",         #科技
        "http://api.iclient.ifeng.com/ClientNews?id=JS83,FOCUSJS83&gv=4.6.5" \
        "&av=0&proid=ifengnews&os=ios_9.1&vt=5&screen=750x1334&publishid=4002" \
        "&uid=086f4de209f0d590a7931bba7584dd5ae8c40064",         #军事
    )

    time = time.time()
    last_time = time - 3600

    def parse(self, response):
        try:
            body = response.body
            body_json = json.loads(body)
            for newsitem in body_json:
                item_list = newsitem.get("item")
                column = newsitem.get("listId")
                print "column: ",column,type(column)
                for item in item_list:
                    if column.startswith("SY"):
                        column = "头条".decode("utf-8")
                    elif column.startswith("YL") or column.startswith("FOCUSYL"):
                        column = "娱乐".decode("utf-8")
                    elif column.startswith("CJ") or column.startswith("FOCUSCJ"):
                        column = "财经".decode("utf-8")
                    elif column.startswith("TY") or column.startswith("FOCUSTY"):
                        column = "体育".decode("utf-8")
                    elif column.startswith("KJ") or column.startswith("FOCUSKJ"):
                        column = "科技".decode("utf-8")
                    elif column.startswith("JS") or column.startswith("FOCUSJS"):
                        column = "军事".decode("utf-8")
                    title = item.get("title")
                    url = item.get("id")
                    comments = item.get("comments")
                    pub_time = item.get("updateTime")
                    pub_time = pub_time.split(' ')
                    pub_time = '-'.join(pub_time[0].split('/')) + ' ' + pub_time[1]
                    img_src = item.get("thumbnail")
                    timearray = time.strptime(pub_time, "%Y-%m-%d %H:%M:%S")
                    timestamp = int(time.mktime(timearray))
                    if timestamp > self.last_time:
                        yield scrapy.Request(url, callback=self.parse_page,meta={'title':title,
                                                'column':column,'comments':comments,'pub_time':pub_time,'img':img_src})
        except Exception, e:
            print 'shixi_zhangshuai@staff.sina.com.cn',
            print '\t',
            print 'fenghuang',
            print '\t',
            print response.url,
            print e

    def parse_page(self,response):
        item = ClientNewsItem()
        now = datetime.datetime.now()
        create_time = now.strftime('%Y-%m-%d %H:%M:%S')
        item['create_time'] = create_time

        body = response.body
        body_json = json.loads(body)
        content = body_json.get("body").get("text")
        source = body_json.get("body").get("source")
        if not content:
            content_list = body_json.get("body").get("slides")[0]
            content = ''
            for item in content_list:
                content += item.get("description")
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
