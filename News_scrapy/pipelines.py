# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class NewsScrapyPipeline(object):
    def __init__(self):
        # FIXME: how can I run multi-spiders by using the same pipelines in a project?
        # if spider.name == 'jixizhixin':
        #     self.f = open('jiqizhixin.json','w')
        #
        # if spider.name == 'xtecher':
        # self.f = open('xtecher.json', 'w')
        pass

    def process_item(self, item, spider):
        # 'a' 追加
        if spider.name == 'jixizhixin':
            self.f = open('jiqizhixin.json', 'a')

        if spider.name == 'xtecher':
            self.f = open('xtecher.json', 'a')

        if spider.name == 'aitists':
            self.f = open('aitists.json', 'a')

        if spider.name == 'zhidx':
            self.f = open('zhidx.json', 'a')

        if spider.name == 'syncedreview':
            self.f = open('syncedreview.json', 'a')

        if spider.name == 'rsarxiv':
            self.f = open('rsarxiv.json', 'a')

        if spider.name == 'neteasetech':
            self.f = open('neteasetech.json', 'a')

        if spider.name == 'cyzone':
            self.f = open('cyzone.json', 'a')

        if spider.name == '36kr':
            self.f = open('36kr.json', 'a')

        if spider.name == 'techreview':
            self.f = open('techreview.json', 'a')

        if spider.name == 'ifeng':
            self.f = open('ifeng.json', 'a')

        if spider.name == 'huxiu':
            self.f = open('huxiu.json', 'a')

        if spider.name == 'dgtle':
            self.f = open('dgtle_new.json', 'a')

        if spider.name == 'aliresearch':
            self.f = open('aliresearch.json', 'a')

        if spider.name == 'techqq':
            self.f = open('techqq.json', 'a')

        if spider.name == 'techsina':
            self.f = open('techsina.json', 'a')

        if spider.name == 'techsohu':
            self.f = open('techsohu.json', 'a')

        if spider.name == 'zaker':
            self.f = open('zaker.json', 'a')

        if spider.name == 'finance_ifeng':
            self.f = open('finance_ifeng.json', 'a')

        if spider.name == 'caixin':
            self.f = open('caixin.json', 'a')

        if spider.name == 'ftchinese':
            self.f = open('ftchinese.json', 'a')

        if spider.name == 'tech2ipo':
            self.f = open('tech2ipo.json', 'a')

        if spider.name == 'infoq':
            self.f = open('infoq.json', 'a')

        if spider.name == 'vcbeat':
            self.f = open('vcbeat.json', 'a')

        if spider.name == 'tmtpost':
            self.f = open('tmtpost.json', 'a')

        if spider.name == 'donews':
            self.f = open('donews.json', 'a')

        if spider.name == 'lijiresearch':
            self.f = open('lijiresearch.json', 'a')

        if spider.name == 'tmtpost':
            self.f = open('tmtpost.json', 'a')

        if spider.name == 'technode':
            self.f = open('technode.json', 'a')

        if spider.name == 'guokr':
            self.f = open('guokr.json', 'a')

        if spider.name == '36dsj':
            self.f = open('36dsj.json', 'a')

        if spider.name == 'sougou':
            self.f = open('sougou.json', 'a')

        if spider.name == 'economist':
            self.f = open('economist.json', 'a')

        # 中文使用unicode编码
        content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.f.write(content)
        return item

    def close_spider(self, spider):
        self.f.close()
