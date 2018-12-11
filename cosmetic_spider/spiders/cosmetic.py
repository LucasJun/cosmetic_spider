# -*- coding: utf-8 -*-
import scrapy
from cosmetic_spider.items import CosmeticItem
from scrapy.conf import settings

class CosmeticSpider(scrapy.Spider):
    name = 'cosmetic'
    # COOKIE = {
    #     'JSESSIONID': 'IP966ND1-TTR06F5C2X5KQ54W3OJH3-B7MDD6PJ-7Z1',
    #     'td_cookie': '3110613103'
    # }
    # cookie = settings['COOKIE']
    allowed_domains = ['http://daji.runcon.cn/index.html']
    start_urls = ['http://daji.runcon.cn/index.html/']

    def parse(self, response):
        item = CosmeticItem()
        item_name_list = response.xpath('//*[@class="cart-table"]/tr/td[1]/a/text()').extract()
        item_count_list = response.xpath('//*[@class="cart-table"]/tr/td[2]/text()').extract()
        for item_name, item_count in zip(item_name_list, item_count_list):
            item['item_name'] = item_name
            item['item_count'] = item_count
            yield item
