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
        # self.sheet.drop()
        # 库存清零，等待更新
        for item in self.sheet.find():
            updateFilter = {'item_name': item['item_name']}
            self.sheet.update_one(filter=updateFilter, update={'$set': {'item_count': 0}})
        print('库存清零')


    def process_item(self, item, spider):
        data = dict(item)
        updateFilter = {'item_name': data['item_name']}
        updateRes = self.sheet.update_one(
            filter=updateFilter,
            update={'$set': data},
            upsert=True)
        # self.sheet.insert(data)
        return updateRes

