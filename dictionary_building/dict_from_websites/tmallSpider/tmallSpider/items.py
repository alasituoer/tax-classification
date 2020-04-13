# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TmallspiderItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    cateTitle = scrapy.Field()
    segName = scrapy.Field()
    segList = scrapy.Field()
