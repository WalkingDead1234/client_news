# # -*- coding: utf-8 -*-
#
# import scrapy
# import json
# from client_news.items import ClientNewsItem
# import time
#
#
# class BaiduImgSpider(scrapy.Spider):
#     name = "baidu_img"
#     allowed_domains = ["baidu.com"]
#
#     start_urls = ["http://api.baiyue.baidu.com/sn/api/medianewslist?pd=newsplus&platform=ios&an=10&ver=1&subtype=1&ln=100&type=image&wf=1&pd=newsplus&sv=5.5.0.1"]
#
#     def parse(self, response):
#         d = json.loads(response.body)
#         last_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - 30 * 60))
#         if d.has_key('data') and d['data'].has_key('news'):
#             for index in range(len(d['data']['news'])):
#                 item = ClientNewsItem()
#                 news = d['data']['news'][index]
#                 if news.has_key('title'):
#                     item['site'] = "百度".decode('utf-8')
#                     item['url'] = news['url']
#                     item['column'] = "图片".decode('utf-8')
#                     item['title'] = news['title']
#                     item['pub_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(news['sourcets'][:-3])))
#                     if item['pub_time'] < last_time_str:
#                         continue
#                     print item['pub_time']
#                     item['source'] = news['site']
#                     whole_content = news['content']
#                     content = ""
#                     for i in range(len(whole_content)):
#                         if type(whole_content[i]['data']) == dict:
#                             if not item.get('img'):
#                                 for value in whole_content[i]['data'].values():
#                                     if type(value) == dict and value.get('small'):
#                                         item['img'] = value['small']['url']
#                                     elif type(value) == dict and value.get('url'):
#                                         item['img'] = value['url']
#                                     elif type(value) == dict and value.get('big'):
#                                         item['img'] = value['big']
#                                     if not content:
#                                         if whole_content[i].get('data') and whole_content[i]['data'].get('text'):
#                                             content = whole_content[i]['data']['text']
#                             continue
#
#                     item['content'] = content
#                     item['sum'] = news['abs']
#
#                     item['tag'] = "no tag"
#                     item['c_count'] = 0
#                     from datetime import datetime
#                     item['create_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                     if not item.get('img'):
#                         item['img'] = "no image"
#                     yield item
#
