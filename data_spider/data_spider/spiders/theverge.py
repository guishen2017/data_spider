import scrapy
import re
import time
import logging
from data_spider.utils.get_date import get_date_list
from data_spider.utils.filter_html import filte
from data_spider.utils.switch_date import switch_time
from data_spider.items import ThevergeItem


class ThevergeSpider(scrapy.Spider):
    name = 'theverge'
    allowed_domains = ['theverge.com']
    start_urls = "https://www.theverge.com/archives/entertainment/{date}"
    logger = logging.getLogger(__name__)

    def start_requests(self):
        date_list = get_date_list(start_str="2014-01-01")
        date_list = list(map(lambda date: str(date).split()[0], date_list))
        date_list = list(map(lambda date: date.replace("-", "/"), date_list))
        date_list = list(map(lambda date: date.replace("/0", "/"), date_list))
        for date in date_list:
            yield scrapy.Request(url=self.start_urls.format(date=date), callback=self.parse)

    def parse(self, response):
        detail_urls = response.xpath("//a[@data-chorus-optimize-field='hed']/@href").getall()
        for detail_url in detail_urls:
            yield scrapy.Request(url=detail_url, callback=self.parse_item)

    def parse_item(self, response):
        try:
            spider_name = self.name
            content = filte("".join(response.xpath("//div[@class='c-entry-content']//text()").getall()))
            image = response.xpath("//picture[@class='c-picture']//img/@src").get()
            images_urls = response.xpath("//div[@class='c-entry-content']//img/@img").getall()
            images_urls.append(image)
            video_urls = response.xpath("//div[@class='c-entry-content']//iframe/@src").getall()
            description = response.xpath("//meta[@name='description']/@content").get()
            posted_at = response.xpath('//time[@class="c-byline__item"]//text()').get().replace("\n", "").replace(" ",
                                                                                                                  "")
            month, day, year = re.findall(r"(.*?)(\d){1,2},(\d+),.*?", posted_at)[0]
            posted_at = switch_time(month, day, year)
            author = response.xpath('//span[@class="c-byline__item"]/a/text()').get()
            source_url = response.url
            title = response.xpath('//h1[@class="c-page-title"]/text()').get()
            tags = ",".join(response.xpath('//li[@class="c-entry-group-labels__item"]//a/span/text()').getall())
            crawl_time = time.strftime("%Y-%m-%d", time.localtime())

            item = ThevergeItem(spider_name=spider_name, content=content, images_urls=images_urls, video_urls=video_urls,
                               description=description, posted_at=posted_at, author=author, source_url=source_url,
                               title=title, tags=tags, crawl_time=crawl_time)
            yield item
        except Exception as e:
            self.logger.debug("Exception:%s" %(e.args))
