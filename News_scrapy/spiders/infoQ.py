# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from News_scrapy.items import NewsItem

# FIXME: crawl page sucessfully (200), but can't get contents, actually can't open json file
class InfoQ(CrawlSpider):
    # 爬虫名
    name = "infoq"
    # 爬取域范围, 允许爬虫在这个域名下进行爬取
    allowed_domains = ["infoq.com",]
    # 起始url列表, 爬虫执行后的第一批请求, 队列处理
    start_urls = ['http://www.infoq.com/cn/']


    rules = (
        # 从起始页提取匹配正则式'/channel/\d{1,3}\.html'的链接，并使用parse来解析
        Rule(LxmlLinkExtractor(allow=(r'/cn/[a-z]+/.+', )), follow=True),
        # 提取匹配'/article/[\d]+.html'的链接，并使用parse_item_yield来解析它们下载后的内容，不递归
        Rule(LxmlLinkExtractor(allow=(r'/cn/news/\d{4}/\d{2}/.+', )), callback='parse_item'),
    )


    def parse_item(self, response):
        item = NewsItem()
        item['url'] = response.url
        item['title'] =  response.xpath('//*[@id="content"]/h1/text()').extract()[0].strip()
        item['pub_time'] = response.url.split('/')[-3] + '-' + response.url.split('/')[-2]
        item['content_code'] = response.xpath('//*[@id="content"]/div[2]/div[1]').extract()[0]

        # 返回每个提取到的item数据, 给管道文件处理, 同时还会回来执行后面的代码
        yield item