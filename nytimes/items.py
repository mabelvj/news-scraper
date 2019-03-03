# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join


class NewsItem(scrapy.Item):
    title = scrapy.Field()
    entry_type = scrapy.Field()
    date = scrapy.Field()
    entry = scrapy.Field()
    url = scrapy.Field()


class NewsLoader(ItemLoader):
    default_output_processor = Join()
