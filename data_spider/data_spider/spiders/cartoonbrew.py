# -*- coding: utf-8 -*-
import scrapy
import time
import logging
from data_spider.utils.filter_html import filte
from data_spider.items import CartoonbrewItem
from data_spider.utils.switch_date import switch_time

class CartoonbrewSpider(scrapy.Spider):
    name = 'cartoonbrew'
    allowed_domains = ['cartoonbrew.com']
    # start_urls = ['http://cartoonbrew.com/']
    shorts_start_url = "https://www.cartoonbrew.com/shorts/page/{}"
    cgi_url = "https://www.cartoonbrew.com/cgi/page/{}"
    film_url = "https://www.cartoonbrew.com/feature-film/page/{}"
    logger = logging.getLogger(__name__)

    def start_requests(self):
        for page in range(1,67):
            yield scrapy.Request(url=self.shorts_start_url.format(page))
        for page in range(1,31):
            yield scrapy.Request(url=self.cgi_url.format(page))
        for page in range(1,84):
            yield scrapy.Request(url=self.film_url.format(page))

    def parse(self, response):
        detail_urls = response.xpath("//h2[@class='entry-title']/a/@href").getall()
        for detail_url in detail_urls:
            yield scrapy.Request(url=detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        try:
            spider_name = self.name
            content = filte("".join(response.xpath('//div[@class="entry-content"]//p//text()').getall()))
            images_urls = response.xpath("//div[@class='entry-content']//img/@src").getall()
            for index in range(len(images_urls)):
                if "==" in images_urls[index] or "data" in images_urls[index]:
                    images_urls.pop(index)
            video_urls = response.xpath('//iframe/@src').getall()
            description = response.xpath("//meta[@property='og:description']/@content").get()
            posted_at = response.xpath('//div[@class="post-inner"]/header//time[@class="updated"]/text()').get()
            month, day, year = posted_at.split(" ")[0].split("/")
            posted_at = switch_time(month=month,day=day,year=year)
            author = response.xpath('//span[@class="author"]/a[@rel="author"]/text()').get()
            crawl_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).split(" ")[0]
            source_url = response.url
            title = response.xpath("//h1[@class='entry-title']//text()").get()
            tags = ",".join(response.xpath("//header/a[@class='category-slug']/text()").getall())

            items = CartoonbrewItem(spider_name=spider_name,content=content,images_urls=images_urls,video_urls=video_urls,
                                    description=description,posted_at=posted_at,author=author,crawl_time=crawl_time,
                                    source_url=source_url,title=title,tags=tags)
            yield items
        except Exception as e:
            self.logger.debug("Exception:%s" % (e.args))