'''pipeline '''

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymongo

class MongoDBPipeline(object):
    def __init__(self, host,user, password):
        self.host = host
        # self.db = db
        self.user = user
        self.password = password
        self.client = pymongo.MongoClient('mongodb://%s:%s@%s/admin' % (self.user,self.password,self.host))

    # def open_spider(self, spider):
    #     """
    #     open spider
    #     :param spider: spider object
    #     :return:
    #     """
    #     self.client = pymongo.MongoClient(self.host)
    #     self.animenews = self.client[self.db]

    def process_item(self, item, spider):
        """
        process item
        :param item: store item
        :param spider: spider object
        :return:
        """
        db_name = item.get_db_name()
        self.collection = self.client[db_name]
        self.collection['content'].insert(dict(item))
        # item = dict(item)
        return item

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get("MONGO_DB"),
            # db=crawler.settings.get("MONGO_DBNAME"),
            user=crawler.settings.get("MONGO_USER"),
            password=crawler.settings.get("MONGO_PASSWORD"),
        )

    def close_spider(self, spider):
        """
        close spider
        :param spider:spider object
        :return:
        """
        self.client.close()

class AnimenewsnetworkDataPipeline():
    '''filte pipeline'''

    def process_item(self, item, spider):
        """
        process data
        :param item: store item
        :param spider: spider object
        :return:
        """
        if spider.name == "animenewsnetwork":
            image_url_list = []
            for image_url in item['images_urls']:
                if ".gif" not in image_url:
                    image_url_list.append(image_url)
            item['images_urls'] = image_url_list
        return item

