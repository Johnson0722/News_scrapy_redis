# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from News_scrapy.items import NewsItem


class Guokr(CrawlSpider):
    # 爬虫名
    name = "guokr"
    # 爬取域范围, 允许爬虫在这个域名下进行爬取
    allowed_domains = ["guokr.com",]
    # 起始url列表, 爬虫执行后的第一批请求, 队列处理
    start_urls = ['http://www.guokr.com/scientific/']


    rules = (
        # 从起始页提取匹配正则式'/channel/\d{1,3}\.html'的链接，并使用parse来解析
        Rule(LxmlLinkExtractor(allow=(r'/scientific/channel/[a-z]+/', )), follow=True),
        # 提取匹配'/article/[\d]+.html'的链接，并使用parse_item_yield来解析它们下载后的内容，不递归
        Rule(LxmlLinkExtractor(allow=(r'/article/\d+/', )), callback='parse_item'),
    )


    def parse_item(self, response):
        item = NewsItem()
        item['url'] = response.url
        item['title'] =  response.xpath('//*[@id="articleTitle"]/text()').extract()[0].strip()
        item['pub_time'] = '2017-01-01'
        item['content_code'] = response.xpath('//*[@id="articleContent"]/div/div[1]').extract()[0]

        # 返回每个提取到的item数据, 给管道文件处理, 同时还会回来执行后面的代码
        yield item