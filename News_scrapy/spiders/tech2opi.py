# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from News_scrapy.items import NewsItem


class Tech2ipo(RedisCrawlSpider):
    # 爬虫名
    name = "tech2ipo"
    # 爬取域范围, 允许爬虫在这个域名下进行爬取
    allowed_domains = ["tech2ipo.com",]
    # 起始url列表, 爬虫执行后的第一批请求, 队列处理
    redis_key = 'tech2ipo:start_urls'
    # start_urls = ['http://tech2ipo.com/',
    #               'http://tech2ipo.com/special/11',
    #               'http://tech2ipo.com/special/12',
    #               'http://tech2ipo.com/special/13',
    #               'http://tech2ipo.com/special/14',
    #               'http://tech2ipo.com/special/1',
    #               'http://tech2ipo.com/special/6',
    #               'http://tech2ipo.com/special/7',
    #               'http://tech2ipo.com/special/8',
    #               'http://tech2ipo.com/special/9',]


    rules = (
        # 从起始页提取匹配正则式'/channel/\d{1,3}\.html'的链接，并使用parse来解析
        Rule(LxmlLinkExtractor(allow=(r'/special/\d+', )), follow=True),
        # 提取匹配'/article/[\d]+.html'的链接，并使用parse_item_yield来解析它们下载后的内容，不递归
        Rule(LxmlLinkExtractor(allow=(r'tech2ipo.com/\d+', )), callback='parse_item'),
    )


    def parse_item(self, response):
        item = NewsItem()
        item['url'] = response.url
        item['title'] =  response.xpath('//*[@id="site-content"]/div/div[2]/h1/text()').extract()[0]
        item['pub_time'] = response.xpath('//*[@id="site-content"]/div/div[1]/div[2]/div/div/div/a[2]/text()').extract()[0][4:]
        item['content_code'] = response.xpath('//*[@id="site-content"]/div/div[3]').extract()[0]

        # 返回每个提取到的item数据, 给管道文件处理, 同时还会回来执行后面的代码
        yield item