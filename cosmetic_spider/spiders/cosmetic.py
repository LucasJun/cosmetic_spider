# -*- coding: utf-8 -*-
import scrapy
from cosmetic_spider.items import CosmeticItem
from scrapy.conf import settings
import time

class CosmeticSpider(scrapy.Spider):
    name = 'cosmetic'
    allowed_domains = ['http://daji.runcon.cn/index.html']

    def start_requests(self):
        headers = settings['DEFAULT_REQUEST_HEADERS']
        cookie = settings['COOKIE'] # cookie写在setting
        start_urls = 'http://daji.runcon.cn/index.html/'
        yield scrapy.Request(url=start_urls, headers=headers, cookies=cookie)

    def price_adjust(self, item_price):
        if item_price > 0 and item_price <=50:
            item_price = item_price + 10    # 不包邮
        # elif item_price > 30 and item_price <= 50:
        #     item_price = item_price + 10 + 11
        elif item_price > 50 and item_price <= 100:
            item_price = item_price + 15    # 不包邮
        elif item_price > 100 and item_price <= 200:
            item_price = item_price + 20 + 11
        elif item_price > 200 and item_price <= 300:
            item_price = item_price + 30 + 11
        elif item_price > 300 and item_price <= 400:
            item_price = item_price + 45 + 7
        elif item_price > 400 and item_price <= 500:
            item_price = item_price + 50 + 7
        elif item_price > 500 and item_price <= 800:
            item_price = item_price + 60 + 7
        elif item_price > 800 and item_price <= 1000:
            item_price = item_price + 80 + 7
        elif item_price > 1000:
            item_price = item_price + 100 + 7
        else:
            pass
        return item_price

    def parse(self, response):
        item = CosmeticItem()
        # item_name_list = response.xpath('//*[@class="cart-table"]/tr/td[1]/a/text()').extract()
        # item_count_list = response.xpath('//*[@class="cart-table"]/tr/td[2]/text()').extract()
        # item_price_list = response.xpath('//*[@class="cart-table"]/tr/td[3]/text()').extract()

        detail_list = response.xpath('//*[@class="cart-table"]/tr')
        for detail in detail_list:
            # 旧版本库存系统的结构，已淘汰
            # try:
            #     item_name = detail.xpath('.//td[1]/a/text()').extract()[0]
            # # 部分item没有图。所以html结构不一样，这里做一个检查,None返回触发IndexError: list index out of range
            # except IndexError:
            #     item_name = detail.xpath('.//td[1]/text()').extract()[0]
            item_name = detail.xpath('.//td[1]/span/text()').extract()[0]
            item_count = detail.xpath('.//td[2]/text()').extract()[0]
            item_price = detail.xpath('.//td[3]/text()').extract()[0]
            # 将item_price从string转换成float
            item_count = int(item_count)
            item_price = float(item_price.replace('￥', '').replace(',', ''))
            item_price = self.price_adjust(item_price)  # 价格调整
            # 将数据送到pipelines
            item['item_name'] = item_name
            item['item_count'] = item_count
            item['item_price'] = item_price
            item['date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            yield item
