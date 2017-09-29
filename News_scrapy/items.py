# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()          # 文章标题
    url = scrapy.Field()            # 文章来源
    content_code = scrapy.Field()   # 文章内容块(HTML代码块)
    pub_time = scrapy.Field()       # 发布时间