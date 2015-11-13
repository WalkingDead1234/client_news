# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from twisted.enterprise import adbapi
import MySQLdb.cursors
import traceback

class ClientNewsPipeline(object):
    def __init__(self):							#初始化连接mysql的数据库相关信息
        self.dbpool = adbapi.ConnectionPool(
            dbapiName='MySQLdb',
            host='10.210.208.48',
            db='crawl_data',
            port=3306,
            user='suda',
            passwd='wlz*od1ps',
            cursorclass=MySQLdb.cursors.DictCursor,
            charset='utf8',
            use_unicode=False
        )

    def process_item(self, item, spider):
        text = ''
        for i in xrange(len(item['content'])):
            text += item['content'][i]
        item['content'] = text
        text = ''
        for i in xrange(len(item['column'])):
            text += item['column'][i]
        item['column'] = text
        self.dbpool.runInteraction(self._conditional_insert, item)
        return item

    def _conditional_insert(self, tx, item):
        sql = """
        insert into t_client_news (site,columns,title,img,pub_time,c_count,url,sum,sources,content,create_time,tag)
        values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
              """

        tx.execute(sql, (item['site'], item['column'], item['title'], item['img'], item['pub_time'],
                         item['c_count'], item['url'], item['sum'], item['source'], item['content'],
                         item['create_time'], item['tag']))



