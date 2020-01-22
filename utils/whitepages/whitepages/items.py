# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WhitepagesItem(scrapy.Item):
    name = scrapy.Field()
    email = scrapy.Field()
    major = scrapy.Field()
