# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class SourceItem(Item):
    source = Field()


class SearchItem(Item):
    title = Field()
    content = Field()
    tenantId = Field()
    indexName = Field()
    dataAnnotation = Field()
    createDate = Field()
    # source = Field()
    url = Field()
    website = Field()



