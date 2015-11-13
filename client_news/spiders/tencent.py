#! /usr/bin/env python
#coding=utf-8
__author__ = '帅'
import scrapy
from client_news.items import ClientNewsItem
import traceback
import time
import re
import json

class TencentSpider(scrapy.Spider):
    name = "tencent"
    allowed_domains = ["qq.com"]
    start_urls = (
        "http://r.inews.qq.com/getQQNewsIndexAndItems?" \
                "uid=cbcbaf294e2388c3&" \
            "Cookie=%20lskey%3D%3B%20luin%3D%3B%20skey%3D%3B%20uin%3D%3B%20logintype%3D0%20&" \
            "qn-rid=319953666&store=202&hw=Meizu_MX4&devid=862095023463703&" \
            "qn-sig=e7ce2b01104982e64891347ab888c48a&screen_width=1152&" \
            "mac=38%253Abc%253A1a%253Ab2%253A7d%253Ae3&chlid=news_news_top&" \
            "appver=19_android_4.7.3&qqnetwork=wifi&" \
            "mid=447dcfe3a8f5a99142f1932b2fb1dce3fd698d3c&imsi=460011171058730&" \
            "apptype=android&screen_height=1920", #头条
        "http://r.inews.qq.com/getQQNewsIndexAndItems?" \
              "uid=cbcbaf294e2388c3&Cookie=%20lskey%3D%3B%20luin%3D%3B%20skey%3D%3B%20uin%3D%3B%20logintype%3D0%20" \
              "&qn-rid=669859536&store=202&hw=Meizu_MX4&devid=862095023463703&qn-sig=ffc682ace79619ad63e2ae0a7fab0b31" \
              "&screen_width=1152&mac=38%253Abc%253A1a%253Ab2%253A7d%253Ae3&chlid=news_news_sports" \
              "&appver=19_android_4.7.3&qqnetwork=wifi&mid=447dcfe3a8f5a99142f1932b2fb1dce3fd698d3c" \
              "&imsi=460014231605566&apptype=android&screen_height=1920",         #体育
        "http://r.inews.qq.com/getQQNewsIndexAndItems?" \
              "uid=cbcbaf294e2388c3&Cookie=%20lskey%3D%3B%20luin%3D%3B%20skey%3D%3B%20uin%3D%3B%20logintype%3D0%20" \
              "&qn-rid=1916898901&store=202&hw=Meizu_MX4&devid=862095023463703&" \
              "qn-sig=118c1144e21ee0046a2a49298e15d56e&screen_width=1152" \
              "&mac=38%253Abc%253A1a%253Ab2%253A7d%253Ae3&chlid=news_news_finance&appver=19_android_4.7.3&" \
              "qqnetwork=wifi&mid=447dcfe3a8f5a99142f1932b2fb1dce3fd698d3c&imsi=460014231605566&apptype=android&" \
              "screen_height=1920",         #财经
        "http://r.inews.qq.com/getQQNewsIndexAndItems?" \
            "mid=447dcfe3a8f5a99142f1932b2fb1dce3fd698d3c&devid=862095023463703&" \
            "mac=38%253Abc%253A1a%253Ab2%253A7d%253Ae3&qqnetwork=wifi&store=203&" \
            "screen_height=1920&Cookie=%20lskey%3D%3B%20luin%3D%3B%20skey%3D%3B%" \
            "20uin%3D%3B%20logintype%3D0%20&apptype=android&hw=Meizu_MX4&appver=21_android_4.7.8&" \
            "chlid=news_news_ent&uid=46dee5df39ac177&screen_width=1152&qn-sig=" \
            "83273ecc8e1effd4c9edc52b21ade194&qn-rid=1089707596&imsi=460014231605566",         #娱乐
        "http://r.inews.qq.com/getQQNewsIndexAndItems?mid=447dcfe3a8f5a99142f1932b2fb1dce3fd698d3c&" \
            "devid=862095023463703&mac=38%253Abc%253A1a%253Ab2%253A7d%253Ae3&qqnetwork=wifi&store=203&" \
            "screen_height=1920&Cookie=%20lskey%3D%3B%20luin%3D%3B%20skey%3D%3B%20uin%3D%3B%20logintype%" \
            "3D0%20&apptype=android&hw=Meizu_MX4&appver=21_android_4.7.8&chlid=news_news_tech&" \
            "uid=46dee5df39ac177&screen_width=1152&qn-sig=2ad42eddd250325a4a72f91708a9f8ae&" \
            "qn-rid=259851719&imsi=460014231605566",          #科技
        "http://r.inews.qq.com/getQQNewsIndexAndItems?" \
            "uid=cbcbaf294e2388c3&Cookie=%20lskey%3D%3B%20luin%3D%3B%20skey%3D%3B%20uin%3D%3B%20logintype%3D0%20" \
            "&store=202&hw=Meizu_MX4&devid=862095023463703&screen_width=1152" \
            "&mac=38%253Abc%253A1a%253Ab2%253A7d%253Ae3&chlid=news_news_mil&appver=19_android_4.7.3&qqnetwork=wifi" \
            "&mid=447dcfe3a8f5a99142f1932b2fb1dce3fd698d3c&imsi=460014231605566&apptype=android&screen_height=1920",#军事
        "http://r.inews.qq.com/getQQNewsIndexAndItems?" \
            "uid=cbcbaf294e2388c3&Cookie=%20lskey%3D%3B%20luin%3D%3B%20skey%3D%3B%20uin%3D%3B%20logintype%3D0%20" \
            "&store=202&hw=Meizu_MX4&devid=862095023463703&screen_width=1152" \
            "&mac=38%253Abc%253A1a%253Ab2%253A7d%253Ae3&chlid=news_video_main&appver=19_android_4.7.3" \
            "&qqnetwork=wifi&mid=447dcfe3a8f5a99142f1932b2fb1dce3fd698d3c&imsi=460014231605566&apptype=android&screen_height=1920",#图片
        )

    time = time.time()
    last_time = time - 36000

    def parse(self, response):
        try:
            body = response.body
            body_json = json.loads(body)
            comment_list = [item.get('comments') for item in body_json.get("idlist")[0].get("ids")]
            json_list = body_json.get("idlist")[0].get("newslist")
            for index,newitem in enumerate(json_list):
                comment = comment_list[index]
                flag = newitem.get("flag")
                if flag == '0':
                    flag = "正常".decode('utf-8')
                elif flag == '1':
                    flag = "独家".decode('utf-8')
                elif flag == '3':
                    flag = "图".decode('utf-8')
                elif flag == '4':
                    flag = "专题".decode('utf-8')
                elif flag == '11':
                    flag = "专辑".decode('utf-8')
                else:
                    flag = "无标签".decode('utf-8')
                column = newitem.get("uinname")
                if column == "news_news_top":
                    column = "头条".decode("utf-8")
                elif column == "news_news_sports":
                    column = "体育".decode("utf-8")
                elif column == "news_news_finance":
                    column = "财经".decode("utf-8")
                elif column == "news_news_ent":
                    column = "娱乐".decode("utf-8")
                elif column == "news_news_mil":
                    column = "军事".decode("utf-8")
                elif column == "news_news_tech":
                    column = "科技".decode("utf-8")
                else:
                    column = "图片".decode("utf-8")
                ptime = newitem.get("time")
                url = newitem.get("url")
                url = url.replace("\\","")
                timearray = time.strptime(ptime, "%Y-%m-%d %H:%M:%S")
                timestamp = int(time.mktime(timearray))
                if timestamp > self.last_time:
                    yield scrapy.Request(url, callback=self.parse_page, meta={'json': newitem,'column':column,'comment': comment,'tag':flag})

        except Exception,e:
            print 'shixi_zhangshuai@staff.sina.com.cn',
            print '\t',
            print 'tencent',
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
            content = response.xpath('//p[@class="text"]//text()').extract()
            if not content:
                content = response.xpath('//p[@class="text image_desc"]//text()').extract()
            img = response.xpath('//p[@align="center"]//img/@src').extract()
            img = ' '.join(img)
            if not img:
                img = "noimg"
            item['url'] = response.url
            item['site'] = '腾讯'.decode('utf-8')
            item['column'] = response.meta['column']
            item['c_count'] = response.meta['comment']
            item['title'] = response.meta['json'].get("title")
            item['sum'] = response.meta['json'].get("abstract")
            item['pub_time'] = response.meta['json'].get("time")
            item['source'] = response.meta['json'].get("source")
            item['img'] = img
            item['tag'] = response.meta['tag']
            item['content'] = content
            return item

        except Exception, e:
            print 'shixi_zhangshuai@staff.sina.com.cn', #此处替换为自己的邮箱
            print '\t',
            print 'tencent',
            print '\t',
            print response.url,
            print e
