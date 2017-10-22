# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from News_scrapy.items import NewsItem



class Huxiu(RedisCrawlSpider):
    # 爬虫名
    name = "huxiu"
    # 爬取域范围, 允许爬虫在这个域名下进行爬取
    allowed_domains = ["huxiu.com"]
    # 起始url列表, 爬虫执行后的第一批请求, 队列处理
    redis_key = 'huxiu:start_urls'
    # start_urls = ['https://www.huxiu.com']


    rules = (
        # 从起始页提取匹配正则式'/channel/\d{1,3}\.html'的链接，并使用parse来解析
        Rule(LxmlLinkExtractor(allow=(r'/channel/\d{1,3}/\.html', )), follow=True),
        # 提取匹配'/article/[\d]+.html'的链接，并使用parse_item_yield来解析它们下载后的内容，不递归
        Rule(LxmlLinkExtractor(allow=(r'/article/\d+\.html', )), callback='parse_item'),
    )


    def parse_item(self, response):
        item = NewsItem()

        item['url'] = response.url
        # get article id
        article_id = response.url.split('/')[-1][:6]
        # generate xpath
        title_xpath = '//*[@id="article' + article_id + '"' + ']/div[2]/div[2]/h1/text()'
        pub_time_xpath = '//*[@id="article' + article_id + '"' + ']/div[2]/div[2]/div[1]/div/span[1]/text()'
        content_xpath = '//*[@id="article_content' + article_id + '"' + ']'

        item['title'] = response.xpath(title_xpath).extract()[0].strip()
        item['pub_time'] = response.xpath(pub_time_xpath).extract()[0].strip()
        item['content_code'] = response.xpath(content_xpath).extract()[0].strip()

        # 返回每个提取到的item数据, 给管道文件处理, 同时还会回来执行后面的代码
        yield item