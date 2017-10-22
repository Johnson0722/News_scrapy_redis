# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from News_scrapy.items import NewsItem


class JiqizhixinSpider(RedisCrawlSpider):
    # 爬虫名
    name = "jiqizhixin"
    # 爬取域范围, 允许爬虫在这个域名下进行爬取
    allowed_domains = ["jiqizhixin.com"]
    # 起始url列表, 爬虫执行后的第一批请求, 队列处理
    redis_key = 'jiqizhixin:start_urls'
    # start_urls = ['http://www.jiqizhixin.com/']


    rules = (
        # 从起始页提取匹配正则式'/channel/\d{1,3}\.html'的链接，并使用parse来解析
        Rule(LxmlLinkExtractor(allow=(r'/categories/[a-z|-]+', )), follow=True),
        # 提取匹配'/article/[\d]+.html'的链接，并使用parse_item_yield来解析它们下载后的内容，不递归
        Rule(LxmlLinkExtractor(allow=(r'/articles/[\d|-]+', )), callback='parse_item'),
    )


    def parse_item(self, response):
        item = NewsItem()

        # extract article info by xpath
        node = response.xpath('//*[@id="articles-show"]/article')
        # get content_div, title, publication time and url
        content_code = response.xpath('//*[@id="js-article-content"]').extract()
        title = node.xpath('./h1/text()').extract()
        pub_time = node.xpath('./div/span/text()').extract()

        item['content_code'] = content_code[0]
        item['title'] = title[0]
        item['pub_time'] = pub_time[0]
        item['url'] = response.url

        # 返回每个提取到的item数据, 给管道文件处理, 同时还会回来执行后面的代码
        yield item
