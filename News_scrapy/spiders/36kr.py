# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from News_scrapy.items import NewsItem


# FIXME: Can't get items using xpath
class Kr(RedisCrawlSpider):
    # 爬虫名
    name = "36kr"
    # 爬取域范围, 允许爬虫在这个域名下进行爬取
    allowed_domains = ["36kr.com"]
    # 起始url列表, 爬虫执行后的第一批请求, 队列处理
    redis_key = '36kr:start_urls'
    # start_urls = ['https://36kr.com/', ]


    rules = (
        # 从起始页提取匹配正则式'/channel/\d{1,3}\.html'的链接，并使用parse来解析
        # Rule(LxmlLinkExtractor(allow=(r'/category/\d{2}/', )), follow=True),
        # 提取匹配'/article/[\d]+.html'的链接，并使用parse_item_yield来解析它们下载后的内容，不递归
        Rule(LxmlLinkExtractor(allow=(r'36kr\.com/p/\d+\.html', )), callback='parse_item'),
    )


    def parse_item(self, response):
        item = NewsItem()
        item['url'] = response.url
        item['title'] = response.xpath('//h1').extract()[0].strip()
        item['pub_time'] = "now"
        item['content_code'] = response.xpath('//section[@class="textblock"]').extract()[0].strip()


        # 返回每个提取到的item数据, 给管道文件处理, 同时还会回来执行后面的代码
        yield item