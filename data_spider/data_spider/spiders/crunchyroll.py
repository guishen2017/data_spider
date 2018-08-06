import time
import random
import scrapy
from data_spider.utils.get_date import get_date_list
from data_spider.utils.filter_html import filte
from data_spider.items import CrunchyrollItem


class CrunchyrollSpider(scrapy.Spider):
    name = 'crunchyroll'
    allowed_domains = ['crunchyroll.com']
    start_urls = ['http://crunchyroll.com/']
    start_urls = "http://www.crunchyroll.com/" \
                 "newsfeed/archive/feature/{time}+{hour}%3A{minute}%3A{second}"

    def start_requests(self):
        date_list = get_date_list()
        for date in date_list:
            hour = random.randint(1, 11)
            minute = random.randint(1, 59)
            second = random.randint(1, 59)
            date = str(date).split()[0]
            url = self.start_urls.format(time=date, hour=hour, minute=minute, second=second) #pylint:disable=E1101
            yield scrapy.Request(url=url)

    def parse(self, response):
        '''parse method'''
        detail_urls = response.xpath("//ul[@class='newsfeed']//li/h2/a/@href").getall()
        for url in detail_urls:
            yield scrapy.Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):#pylint:disable=R0201
        '''parse_detail method'''
        title = response.xpath('//div[@class="related"]/h2/a/text()').get("")
        content = "".join(response.xpath('//div[@class="contents"][1]//text()').getall())
        content = filte(content)
        images = response.xpath('//div[@class="contents"][1]//img/@src').getall()
        videos = ""
        description = response.xpath('//div[@class="showcrunchy\
        news_article white-wrapper"]/h2/text()').get("")
        author = response.xpath('//div[@class="byline"]/a[@class="text-link"]/text()').get()
        posted_on = response.xpath('//span[@class="post-date"]/text()').get()
        crawl_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        source_url = response.url
        item = CrunchyrollItem()
        item['title'] = title
        item['content'] = content
        item['images'] = images
        item['videos'] = videos
        item['description'] = description
        item['author'] = author
        item['posted_on'] = posted_on
        item['crawl_time'] = crawl_time
        item['source_url'] = source_url
        yield item

