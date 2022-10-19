# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
import json
from itemadapter import ItemAdapter


class ScraperPipeline:

    collection_name = 'bulldog_jobs'

    def __init__(self, mongo_db, mongo_uri):
        self.mongo_db = mongo_db
        self.mongo_uri = mongo_uri

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items'),
            mongo_uri=crawler.settings.get('MONGO_URI'),
        )

    def open_spider(self, spider):
        self.file = open('result.json', 'w')
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.file.close()
        self.client.close()

    def process_item(self, item, spider):
        record = json.dumps(dict(item)) + "\n"
        self.file.write(record)
        # what is a better way to convert item to json format
        # record1 = str(ItemAdapter(item).asdict()) + "\n"
        
        # if not self.db[self.collection_name].find_one({'link': ItemAdapter(item).asdict()['link']}):
        #     self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item
