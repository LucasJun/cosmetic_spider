# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings

class CosmeticSpiderPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']
        sheetname = settings['MONGODB_SHEETNAME']
        # 创建数据库连接
        client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库
        db = client[dbname]
        # 存放数据的数据库表名
        self.sheet = db[sheetname]
        # 清空旧表
        self.sheet.drop()

    def process_item(self, item, spider):
        data = dict(item)
        updateFilter = {'item_name': data['item_name']}
        updateRes = self.sheet.update_one(
            filter=updateFilter,
            update={'$set': data},
            upsert=True)
        # self.sheet.insert(data)
        return updateRes

# 官方文档实例，不完整
# class MongoPipeline(object):
#
#     collection_name = 'COSMETIC_DATA'
#
#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get('MONGO_URI'),
#             mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
#         )
#
#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]