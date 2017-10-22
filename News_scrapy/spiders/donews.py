# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from News_scrapy.items import NewsItem


class Donews(RedisCrawlSpider):
    # 爬虫名
    name = "donews"
    # 爬取域范围, 允许爬虫在这个域名下进行爬取
    allowed_domains = ["donews.com",]
    # 起始url列表, 爬虫执行后的第一批请求, 队列处理
    redis_key = 'donews:start_urls'
    # start_urls = ['http://www.donews.com/', 'http://www.donews.com/idonews/']


    rules = (
        # 从起始页提取匹配正则式'/channel/\d{1,3}\.html'的链接，并使用parse来解析
        Rule(LxmlLinkExtractor(allow=(r'donews.com/[a-z]+/index', )), follow=True),
        # 提取匹配'/article/[\d]+.html'的链接，并使用parse_item_yield来解析它们下载后的内容，不递归
        Rule(LxmlLinkExtractor(allow=(r'donews.com/news/detail/\d/\d+\.html',
                                      r'/article/detail/\d+/\d+\.html')), callback='parse_item'),
    )


    def parse_item(self, response):
        item = NewsItem()
        item['url'] = response.url
        item['title'] =  response.xpath('//*[@id="main"]/div[2]/h2/text()').extract()[0]
        item['pub_time'] = response.xpath('//*[@id="main"]/div[2]/div[1]/p/span[2]/text()').extract()[0]
        item['content_code'] = response.xpath('//*[@id="main"]/div[2]/div[2]').extract()[0]

        # 返回每个item
        yield item