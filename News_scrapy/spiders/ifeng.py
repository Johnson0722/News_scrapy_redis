# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from News_scrapy.items import NewsItem


class ifeng(RedisCrawlSpider):
    # 爬虫名
    name = "ifeng"
    # 爬取域范围, 允许爬虫在这个域名下进行爬取
    allowed_domains = ["tech.ifeng.com"]
    # 起始url列表, 爬虫执行后的第一批请求, 队列处理
    redis_key = "ifeng:start_urls"
    # start_urls = ['http://tech.ifeng.com/']


    rules = (
        # 从起始页提取匹配正则式'/channel/\d{1,3}\.html'的链接，并使用parse来解析
        Rule(LxmlLinkExtractor(allow=(r'/listpage/\d{5}/\d/.+', )), follow=True),
        # 提取匹配'/article/[\d]+.html'的链接，并使用parse_item_yield来解析它们下载后的内容，不递归
        Rule(LxmlLinkExtractor(allow=(r'/a/\d{8}/[\d|_]+\.shtml', )), callback='parse_item'),
    )


    def parse_item(self, response):
        item = NewsItem()

        item['url'] = response.url
        item['title'] = response.xpath('//*[@id="artical_topic"]/text()').extract()[0].strip()
        item['pub_time'] = response.xpath('//*[@id="artical_sth"]/p/span[1]/text()').extract()[0].strip()
        item['content_code'] = response.xpath('//*[@id="main_content"]').extract()[0].strip()

        # 返回每个提取到的item数据, 给管道文件处理, 同时还会回来执行后面的代码
        yield item
