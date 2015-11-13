# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ClientNewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    site = scrapy.Field()
    url = scrapy.Field()
    column = scrapy.Field()
    title = scrapy.Field()
    pub_time = scrapy.Field()
    source = scrapy.Field()
    content = scrapy.Field()
    img = scrapy.Field()
    sum = scrapy.Field()
    tag = scrapy.Field()
    c_count = scrapy.Field()
    create_time = scrapy.Field()
    pass
