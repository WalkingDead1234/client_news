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
    name = "sina_photo"
    allowed_domains = ["sina.cn"]
    start_urls = (
        "http://api.sina.cn/sinago/list.json?chwm=3023_0001&uid=de07814d33c06fc857f1d01d60d54b571940d87d" \
                "&wm=b207&from=6048393012&connection_type=2&platfrom_version=9.1&p=1&channel=hdpic_toutiao" \
                "&user_uid=&adid=de07814d33c06fc857f1d01d60d54b57&s=20&IDFA=92090EFD-1567-4AD5-AEB3-E8261EBADF17", #精选
        "http://api.sina.cn/sinago/list.json?chwm=3023_0001&uid=de07814d33c06fc857f1d01d60d54b571940d87d" \
                "&wm=b207&from=6048393012&connection_type=2&platfrom_version=9.1" \
                "&p=1&channel=hdpic_funny&user_uid=&adid=de07814d33c06fc857f1d01d60d54b57" \
                "&s=20&IDFA=92090EFD-1567-4AD5-AEB3-E8261EBADF17", #奇趣
        "http://api.sina.cn/sinago/list.json?chwm=3023_0001&uid=de07814d33c06fc857f1d01d60d54b571940d87d" \
                "&wm=b207&from=6048393012&connection_type=2&platfrom_version=9.1&p=1&channel=hdpic_pretty" \
                "&user_uid=&adid=de07814d33c06fc857f1d01d60d54b57&s=20&IDFA=92090EFD-1567-4AD5-AEB3-E8261EBADF17", #明星
        "http://api.sina.cn/sinago/list.json?chwm=3023_0001&uid=de07814d33c06fc857f1d01d60d54b571940d87d" \
                "&wm=b207&from=6048393012&connection_type=2&platfrom_version=9.1&p=1&channel=hdpic_story" \
                "&user_uid=&adid=de07814d33c06fc857f1d01d60d54b57&s=20&IDFA=92090EFD-1567-4AD5-AEB3-E8261EBADF17" #竞技
    )
    time = time.time()
    last_time = time - 36000

    def parse(self, response):
        try:
            body = response.body
            body_json = json.loads(body)
            json_list = body_json["data"]["list"]
            for item0 in json_list:
                title = item0.get("title")
                source = item0.get("source")
                pubdate = item0.get("pubDate")
                pub_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(pubdate))
                print "pub_time: ",pub_time
                comment = item0.get("comment")
                url = item0.get("link")
                url = url.replace("\\","")
                print "url: ",url
                img_src = item0.get("pic")
                img_src = img_src.replace("\\","")
                summary = item0.get("intro")
                #print "summary: ",summary
                timearray = time.strptime(pub_time, "%Y-%m-%d %H:%M:%S")
                timestamp = int(time.mktime(timearray))
                if timestamp > self.last_time:
                    print '---hello---'
                    yield scrapy.Request(url, callback=self.parse_img, meta={'title':title,'source':source,'img':img_src,
                                                                              'summary':summary,'comment':comment,'pub_time':pub_time})
        except Exception, e:
            print 'shixi_zhangshuai@staff.sina.com.cn',
            print '\t',
            print 'sina',
            print '\t',
            print response.url,
            print e

    def parse_img(self,response):
        item = ClientNewsItem()
        now = datetime.datetime.now()
        print "now: ",now
        create_time = now.strftime('%Y-%m-%d %H:%M:%S')
        item['create_time'] = create_time
        item['tag'] = 'notag'
        item['column'] = '图片'.decode("utf-8")

        try:
            #content = response.xpath('//p[@class="describ j_des_txt]//text()').extract()
            content = response.xpath('//p[@class="imgWrap j_img"]//img/@alt').extract()
            if not content:
                content = response.meta['summary']
            print "content: ",content
            item['url'] = response.url
            item['site'] = '新浪'.decode('utf-8')
            item['title'] = response.meta['title']
            item['pub_time'] = response.meta['pub_time']
            item['source'] = response.meta['source']
            item['img'] = response.meta['img']
            item['c_count'] = response.meta['comment']
            item['sum'] = response.meta['summary']
            item['content'] = content
            return item

        except Exception, e:
            print 'shixi_zhangshuai@staff.sina.com.cn',
            print '\t',
            print 'sina',
            print '\t',
            print response.url,
            print e

