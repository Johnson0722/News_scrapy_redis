# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class NewsScrapyPipeline(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        self.name = spider.name
        # 'a' 追加
        self.f = open(spider.name + '.json', 'a')

    def process_item(self, item, spider):

        # 中文使用unicode编码
        content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.f.write(content)
        return item

    def close_spider(self, spider):
        self.f.close()
