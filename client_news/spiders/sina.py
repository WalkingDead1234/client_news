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

class SinaSpider(scrapy.Spider):
    name = "sina"
    allowed_domains = ["sina.cn"]
    start_urls = (
        "http://api.sina.cn/sinago/list.json?" \
                "uid=827ba542c56e2afe&loading_ad_timestamp=0&platfrom_version=4.4.2&" \
                "wm=b207&imei=862095023463703&from=6048095012&connection_type=2&" \
                "chwm=12010_0001&AndroidID=d74593446f07c887ef46c8a3cdcfc8bc&v=1" \
                "&s=40&IMEI=bb0db9e9b59d1e567d23698224ffa26a&" \
                "p=1&MAC=cc76d3d0be07a7df4f1b54173d1db9a2&channel=news_toutiao",  #头条
        "http://api.sina.cn/sinago/list.json?uid=827ba542c56e2afe&loading_ad_timestamp=0&platfrom_version=4.4.2" \
                  "&wm=b207&oldchwm=12010_0001&imei=862095023463703&from=6048095012&connection_type=2" \
                  "&chwm=12010_0001&AndroidID=d74593446f07c887ef46c8a3cdcfc8bc&v=1&s=40" \
                  "&IMEI=bb0db9e9b59d1e567d23698224ffa26a&p=%d&user_id=1653882532&MAC=cc76d3d0be07a7df4f1b54173d1db9a2" \
                  "&channel=news_sports",         #体育
        "http://api.sina.cn/sinago/list.json?uid=827ba542c56e2afe&loading_ad_timestamp=0&platfrom_version=4.4.2" \
                  "&wm=b207&oldchwm=12010_0001&imei=862095023463703&from=6048095012&connection_type=2" \
                  "&chwm=12010_0001&AndroidID=d74593446f07c887ef46c8a3cdcfc8bc&v=1&s=40" \
                  "&IMEI=bb0db9e9b59d1e567d23698224ffa26a&p=%d&user_id=1653882532&MAC=cc76d3d0be07a7df4f1b54173d1db9a2" \
                  "&channel=news_finance",         #财经
        "http://api.sina.cn/sinago/list.json?chwm=12010_0001" \
                      "&s=20&MAC=cc76d3d0be07a7df4f1b54173d1db9a2&wm=b207&platfrom_version=5.0.1&loading_ad_timestamp=0" \
                      "&from=6048195012&AndroidID=a78b2a4a0d2d1bea8df1da87d2ffed48&IMEI=bb0db9e9b59d1e567d23698224ffa26a&v=1&connection_type=2" \
                      "&imei=862095023463703&p=%d&uid=827ba542c56e2afe&channel=news_ent",         #娱乐
        "http://api.sina.cn/sinago/list.json?chwm=12010_0001&s=20&MAC=cc76d3d0be07a7df4f1b54173d1db9a2&wm=b207&platfrom_version=5.0.1&user_uid=1653882532&loading_ad_timestamp=0&from=6048195012&AndroidID=a78b2a4a0d2d1bea8df1da87d2ffed48&oldchwm=12010_0001&IMEI=bb0db9e9b59d1e567d23698224ffa26a&v=1&connection_type=2&imei=862095023463703" \
                      "&p=%d&uid=827ba542c56e2afe&channel=news_tech"          #科技
        "http://api.sina.cn/sinago/list.json?chwm=3023_0001&uid=de07814d33c06fc857f1d01d60d54b571940d87d" \
                    "&wm=b207&from=6048393012&connection_type=2&platfrom_version=9.1&p=1&channel=news_mil" \
                    "&user_uid=&adid=de07814d33c06fc857f1d01d60d54b57&s=20" \
                    "&IDFA=92090EFD-1567-4AD5-AEB3-E8261EBADF17" #军事
    )

    time = time.time()
    last_time = time - 3600

    def parse(self, response):
        try:
            body = response.body
            body_json = json.loads(body)
            json_list = body_json["data"]["list"]
            for item in json_list:
                title = item.get("title")
                source = item.get("source")
                pubdate = item.get("pubDate")
                pub_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(pubdate))
                comment = item.get("comment")
                url = item.get("link")
                url = url.replace("\\","")
                img_src = item.get("pic")
                img_src = img_src.replace("\\","")
                timearray = time.strptime(pub_time, "%Y-%m-%d %H:%M:%S")
                timestamp = int(time.mktime(timearray))
                if timestamp > self.last_time:
                    yield scrapy.Request(url, callback=self.parse_page, meta={'title':title,'source':source,'img':img_src,
                                                                              'comment':comment,'pub_time':pub_time})
        except Exception, e:
            print 'shixi_zhangshuai@staff.sina.com.cn',
            print '\t',
            print 'sina',
            print '\t',
            print response.url,
            print e

    def parse_page(self, response):
        item = ClientNewsItem()
        now = datetime.datetime.now()
        create_time = now.strftime('%Y-%m-%d %H:%M:%S')
        item['create_time'] = create_time
        item['tag'] = 'notag'
        try:
            content = response.xpath('//p[@class="art_t"]//text()').extract()
            if not content:
                content = response.xpath('//div[@class="art_t"]//text()').extract()
            summary = response.xpath('//meta[@name="description"]/@content').extract()
            column = response.xpath('//ul[@class="h_nav_items"]//li/a/text()').extract()[0]
            #print "type: ",type(column)
            if column == "首页":
                column = "头条".decode("utf-8")
            item['url'] = response.url
            item['site'] = '新浪'.decode('utf-8')
            item['column'] = column
            item['title'] = response.meta['title']
            item['pub_time'] = response.meta['pub_time']
            item['source'] = response.meta['source']
            item['img'] = response.meta['img']
            item['c_count'] = response.meta['comment']
            item['sum'] = summary
            item['content'] = content
            return item

        except Exception, e:
            print 'shixi_zhangshuai@staff.sina.com.cn',
            print '\t',
            print 'netease',
            print '\t',
            print response.url,
            print e






