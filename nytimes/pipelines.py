# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime


def process_date(d):
    formats = ['%b. %d, %Y', '%A, %b. %d, %Y', '%A, %B %d, %Y', '%B %d, %Y']
    for fmt in formats:
        try:
            return datetime.datetime.strptime(d,
                                              fmt).strftime('%Y-%m-%d')
        except:
            pass
    raise ValueError('no valid date format found: %s' % d)


class NewsPipeline(object):
    def process_item(self, item, spider):
        item['date'] = process_date(item['date'])
        item.save(commit=True)
        return item
