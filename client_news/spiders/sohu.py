# -*- coding: utf-8 -*-
__author__ = 'xiutx'
# __mod__ = 'yufeng11_20151109'
import scrapy
from client_news.items import ClientNewsItem
import traceback
import time
import re
import json
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 

class SohuSpider(scrapy.Spider):
    name = "sohu"
    allowed_domains = ["sohu.com"]
    start_urls = (
       "http://api.k.sohu.com/api/channel/v5/news.go?channelId=1&num=20&imgTag=1&showPic=1&picScale=11&rt=json&net=wifi&cdma_lat=39.993918&cdma_lng=116.307304&from=channel&page=1&action=0&mode=0&cursor=0&mainFocalId=0&focusPosition=1&viceFocalId=0&lastUpdateTime=0&gbcode=110000&p1=NjA2OTMwMDk3NzY3NTQ0ODM1Mg%3D%3D&gid=02ffff11061111575f246a9f15ccd153a74ee89d53b53b&pid=-1",
       "http://api.k.sohu.com/api/channel/v5/news.go?channelId=2&num=20&imgTag=1&showPic=1&picScale=11&rt=json&net=wifi&cdma_lat=39.993918&cdma_lng=116.307304&from=channel&page=1&action=0&mode=0&cursor=0&mainFocalId=0&focusPosition=1&viceFocalId=0&lastUpdateTime=0&gbcode=110000&p1=NjA2OTMwMDk3NzY3NTQ0ODM1Mg%3D%3D&gid=02ffff11061111575f246a9f15ccd153a74ee89d53b53b&pid=-1",
       "http://api.k.sohu.com/api/channel/v5/news.go?channelId=3&num=20&imgTag=1&showPic=1&picScale=11&rt=json&net=wifi&cdma_lat=39.993918&cdma_lng=116.307304&from=channel&page=1&action=0&mode=0&cursor=0&mainFocalId=0&focusPosition=1&viceFocalId=0&lastUpdateTime=0&gbcode=110000&p1=NjA2OTMwMDk3NzY3NTQ0ODM1Mg%3D%3D&gid=02ffff11061111575f246a9f15ccd153a74ee89d53b53b&pid=-1",
       "http://api.k.sohu.com/api/channel/v5/news.go?channelId=4&num=20&imgTag=1&showPic=1&picScale=11&rt=json&net=wifi&cdma_lat=39.993918&cdma_lng=116.307304&from=channel&page=1&action=0&mode=0&cursor=0&mainFocalId=0&focusPosition=1&viceFocalId=0&lastUpdateTime=0&gbcode=110000&p1=NjA2OTMwMDk3NzY3NTQ0ODM1Mg%3D%3D&gid=02ffff11061111575f246a9f15ccd153a74ee89d53b53b&pid=-1",
       "http://api.k.sohu.com/api/channel/v5/news.go?channelId=5&num=20&imgTag=1&showPic=1&picScale=11&rt=json&net=wifi&cdma_lat=39.993918&cdma_lng=116.307304&from=channel&page=1&action=0&mode=0&cursor=0&mainFocalId=0&focusPosition=1&viceFocalId=0&lastUpdateTime=0&gbcode=110000&p1=NjA2OTMwMDk3NzY3NTQ0ODM1Mg%3D%3D&gid=02ffff11061111575f246a9f15ccd153a74ee89d53b53b&pid=-1",
       "http://api.k.sohu.com/api/channel/v5/news.go?channelId=6&num=20&imgTag=1&showPic=1&picScale=11&rt=json&net=wifi&cdma_lat=39.993918&cdma_lng=116.307304&from=channel&page=1&action=0&mode=0&cursor=0&mainFocalId=0&focusPosition=1&viceFocalId=0&lastUpdateTime=0&gbcode=110000&p1=NjA2OTMwMDk3NzY3NTQ0ODM1Mg%3D%3D&gid=02ffff11061111575f246a9f15ccd153a74ee89d53b53b&pid=-1",
       "http://api.k.sohu.com/api/photos/listInChannel.go?rt=json&channelId=47&pageSize=20&pageNo=1&offset=-1&p1=NjA2OTMwMDk3NzY3NTQ0ODM1Mg%3D%3D&gid=02ffff11061111575f246a9f15ccd153a74ee89d53b53b&pid=-1",
    )
    time = time.time()
    last_time = time - 3600
    def parse(self, response): #解析方法，调用的时候传入从每一个URL传回的Response对象作为唯一参数，负责解析并匹配抓取的数据(解析为item)，跟踪更多的URL
        try:
            body = response.body
            body_json = json.loads(body)          
            if body_json.has_key( 'articles'):
                json_list= body_json.get( "articles" ) #首页，体育，娱乐，财经，军事，科技
                tname= body_json.get( 'channelName' )
                for newitem in json_list:
                    url=""
                    updateTime= newitem.get("updateTime")
                    newsId= newitem.get("newsId")
                    ptime= newitem.get('time')
                    if not updateTime or not newsId or int(updateTime)<=0 : continue
                    url="http://zcache.k.sohu.com/api/news/cdn/v1/article.go/"+str(newsId)+"/0/613/0/3/1/12/31/3/1/1/"+str(updateTime)+".xml"
                    if url:
                        if int(ptime)> self.last_time:
                            yield scrapy.Request(url, callback=self.parse_page, meta={'json': newitem, 'column': tname})
            if body_json.has_key( 'news'):
                json_list= body_json.get( 'news' ) #美图
                tname= body_json.get( 'shareRead' ).get('from')
                for newitem in json_list:
                    url=""
                    gid= newitem.get( "gid" )
                    ptime= newitem.get('time')
                    if not gid or int(gid)<=0: continue
                    url= "http://api.k.sohu.com/api/photos/gallery.go?&gid="+str(gid)+"&openType=0&channelId=47&zgid=02ffff11061111575f246a9f15ccd153a74ee89d53b53b&from=news&fromId=null&showSdkAd=1&supportTV=1&refer=3&p1=NjA2OTMwMDk3NzY3NTQ0ODM1Mg%3D%3D&pid=-1"
                    if url:
                        if int(ptime)> self.last_time:
                            yield scrapy.Request(url, callback=self.parse_page1, meta={'json': newitem, 'column': tname})

        except Exception, e:
            print 'yufeng11@staff.sina.com.cn', #此处替换为自己的邮箱
            print '\t',
            print 'sohu',
            print '\t',
            print response.url,
            print e

    def parse_page(self, response):
        item = ClientNewsItem()
        now = datetime.datetime.now()
        create_time = now.strftime('%Y-%m-%d %H:%M:%S')
        item['create_time'] = create_time

        try:
            content = response.xpath('//root/content/text()').extract()
            if not content:content=['nocontent']
            content1=""
            p=re.compile( "[^\u4E00-\u9FFF]+" )  #匹配非中文字符的正则模式
            g= p.findall( content[0] ) #返回中文字符串
            if not g: g='nocontent'
            for ele in g:
                if len(ele)>=4:
                    content1+= ele
            source= response.xpath( '//root/shareRead/from/text()').extract()
            time= response.xpath( '//root/time/text()' ).extract()
            if not time: time='notime'
            time= time[0].replace( "/","-" )
            tag = response.meta['json'].get("iconText")
            img= response.meta['json'].get("pics")
            sum1= response.meta['json'].get("description")
            if not tag: tag ='notag'
            if not img: img=[ 'noimg' ]
            if not sum1: sum1='nosum'
            if not source: source='nosource'
            item['url'] = response.url
            item['site'] = '搜狐'.decode('utf-8')
            item['column'] = response.meta['column']
            item['title'] = response.meta['json'].get("title")
            item['pub_time'] = time
            item['source'] = source                
            item['c_count'] = response.meta['json'].get("commentNum")
            item['tag'] = tag

            item['content'] = content1
            item['img'] = img[0]
            item['sum'] = sum1
            return item

        except Exception, e:
            print 'yufeng11@staff.sina.com.cn', #此处替换为自己的邮箱
            print '\t',
            print 'sohu',
            print '\t',
            print response.url,
            print e

    def parse_page1(self, response):
        item = ClientNewsItem()
        now = datetime.datetime.now()
        create_time = now.strftime('%Y-%m-%d %H:%M:%S')
        item['create_time'] = create_time

        try:
            time= response.xpath( '//root/time/text()' ).extract()
            sum1= response.xpath( '//root/gallery/abstract/text()' ).extract()
            content= response.xpath( '//root/shareRead/description/text()' ).extract()
            # print 
            if not content: content=[ 'nocontent' ]
            content1=""
            p=re.compile( "[^\u4E00-\u9FFF]+" )  #匹配非中文字符的正则模式
            g= p.findall( content[0] )
            if not g: g=['nocontent']
            if not sum1: sum1='nosum'
            if not time: time=['notime']
            for ele in g:
                if len(ele)>=4:
                    content1+= ele
            time= time[0].replace( "/","-" )
            item['url'] = response.url
            item['site'] = '搜狐'.decode('utf-8')
            item['column'] = response.meta['column']
            item['title'] = response.meta['json'].get("title")
            item['pub_time'] = time
            item['source'] = "nosource"
            item['img'] = response.meta['json'].get("images")[0]
            item['c_count'] = response.meta['json'].get("commentNum")
            item['sum'] = sum1
            item['tag'] = "notag"
            item['content'] = content1

            return item

        except Exception, e:
            print 'yufeng11@staff.sina.com.cn', #此处替换为自己的邮箱
            print '\t',
            print 'sohu',
            print '\t',
            print response.url,
            print e
