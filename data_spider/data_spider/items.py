# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AnimenewsItem(scrapy.Item):
    """
    store item
    """
    title = scrapy.Field()
    content = scrapy.Field()
    images_urls = scrapy.Field()
    video_urls = scrapy.Field()
    description = scrapy.Field()
    posted_at = scrapy.Field()
    author = scrapy.Field()
    crawl_time = scrapy.Field()
    update_time = scrapy.Field()
    source_url = scrapy.Field()
    type = scrapy.Field()

    def get_db_name(self):
        return "animenews"
    # mongodb_name = "animenews"

class CrunchyrollItem(scrapy.Item):# pylint: disable=too-many-ancestors
    '''define CrunchyrollItem'''
    title = scrapy.Field()
    content = scrapy.Field()
    images = scrapy.Field()
    videos = scrapy.Field()
    description = scrapy.Field()
    author = scrapy.Field()
    posted_on = scrapy.Field()
    crawl_time = scrapy.Field()
    source_url = scrapy.Field()

    def get_db_name(self):
        return "crunchyroll"
    # mongodb_name = "crunchyroll"

class OtakumodeItem(scrapy.Item):
    """
    define item class
    """
    title = scrapy.Field()
    content = scrapy.Field()
    images_urls = scrapy.Field()
    video_urls = scrapy.Field()
    description = scrapy.Field()
    posted_at = scrapy.Field()
    crawl_time = scrapy.Field()
    source_url = scrapy.Field()
    type = scrapy.Field()
    tags = scrapy.Field()

    def get_db_name(self):
        return "otakumode"

class PolygonItem(scrapy.Item):
    # PolygonItem Item
    spider_name = scrapy.Field()
    content = scrapy.Field()
    images_urls = scrapy.Field()
    video_urls = scrapy.Field()
    description = scrapy.Field()
    posted_at = scrapy.Field()
    author = scrapy.Field()
    crawl_time = scrapy.Field()
    source_url = scrapy.Field()
    title = scrapy.Field()
    tags = scrapy.Field()

    def get_db_name(self):
        return "polygon"

class ThevergeItem(scrapy.Item):
    # ThevergeItem Item
    spider_name = scrapy.Field()
    content = scrapy.Field()
    images_urls = scrapy.Field()
    video_urls = scrapy.Field()
    description = scrapy.Field()
    posted_at = scrapy.Field()
    author = scrapy.Field()
    crawl_time = scrapy.Field()
    source_url = scrapy.Field()
    title = scrapy.Field()
    tags = scrapy.Field()

    def get_db_name(self):
        return "theverge"

class AwnItem(scrapy.Item):
    # ThevergeItem Item
    spider_name = scrapy.Field()
    content = scrapy.Field()
    images_urls = scrapy.Field()
    video_urls = scrapy.Field()
    description = scrapy.Field()
    posted_at = scrapy.Field()
    author = scrapy.Field()
    crawl_time = scrapy.Field()
    source_url = scrapy.Field()
    title = scrapy.Field()
    tags = scrapy.Field()

    def get_db_name(self):
        return "awn"

class CartoonbrewItem(scrapy.Item):
    # ThevergeItem Item
    spider_name = scrapy.Field()
    content = scrapy.Field()
    images_urls = scrapy.Field()
    video_urls = scrapy.Field()
    description = scrapy.Field()
    posted_at = scrapy.Field()
    author = scrapy.Field()
    crawl_time = scrapy.Field()
    source_url = scrapy.Field()
    title = scrapy.Field()
    tags = scrapy.Field()

    def get_db_name(self):
        return "cartoonbrew"
