# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CosmeticItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 商品名
    item_name = scrapy.Field()
    # 商品库存
    item_count = scrapy.Field()
    # 商品价格
    item_price = scrapy.Field()
    # 更新日期
    date = scrapy.Field()
    pass
