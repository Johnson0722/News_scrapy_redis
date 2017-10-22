# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from News_scrapy.items import NewsItem


class Vcbeat(RedisCrawlSpider):
    # 爬虫名
    name = "vcbeat"
    # 爬取域范围, 允许爬虫在这个域名下进行爬取
    allowed_domains = ["vcbeat.net",]
    # 起始url列表, 爬虫执行后的第一批请求, 队列处理
    redis_key = "vcbeat:start_urls"
    # start_urls = ['http://vcbeat.net/', 'http://vcbeat.net/Series/seriesIndex']


    rules = (
        # 从起始页提取匹配正则式'/channel/\d{1,3}\.html'的链接，并使用parse来解析
        Rule(LxmlLinkExtractor(allow=(r'/seriesD/\d{1,2}', )), follow=True),
        # 提取匹配'/article/[\d]+.html'的链接，并使用parse_item_yield来解析它们下载后的内容，不递归
        Rule(LxmlLinkExtractor(allow=(r'vcbeat\.net/.+=', )), callback='parse_item'),
    )


    def parse_item(self, response):
        item = NewsItem()
        item['url'] = response.url
        item['title'] =  response.xpath('//*[@id="article_title"]/p/text()').extract()[0].strip()
        item['pub_time'] = response.xpath('//*[@id="article_title"]/div/span[2]/text()').extract()[0]
        item['content_code'] = response.xpath('/html/body/div[7]/div/div[1]/div[1]').extract()[0]

        # 返回每个提取到的item数据, 给管道文件处理, 同时还会回来执行后面的代码
        yield item