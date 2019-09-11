# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from scrapy import Item


class SourcePipeline(object):
    pass


class MongoDBPipeline:
    def open_spider(self, spider):
        db_uri = spider.settings.get('MONGODB_URI', 'mongodb://localhost:27017')
        db_name = spider.settings.get('MONGODB_DB_NAME')

        self.db_client = MongoClient(db_uri)
        self.db = self.db_client[db_name]

    def close_spider(self, spider):
        self.db_client.close()

    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    def insert_db(self, item):
        if isinstance(item, Item):
            item = dict(item)
        collection = self.db['search_tenant_'+str(item['tenantId'])]
        collection.update({'url': item['url'], 'title': item['title']}, {'$set': item}, True)
        # TODO



        # self.db.cosmoplat_search.insert_one(item)
