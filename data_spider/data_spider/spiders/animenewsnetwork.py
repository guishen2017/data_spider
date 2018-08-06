import time
import re
import scrapy
from data_spider.utils.get_date import get_date_list
from data_spider.utils.filter_html import filte
from data_spider.items import AnimenewsItem

class AnimenewsnetworkSpider(scrapy.Spider):
    name = 'animenewsnetwork'
    allowed_domains = ['animenewsnetwork.com']
    start_urls = ['https://www.animenewsnetwork.com/']
    ajax_url = "https://www.animenewsnetwork.com/herald/hp_more?d={day}"
    today = time.strftime("%Y-%m-%d", time.localtime())

    # custom_settings = {
    #     "ITEM_PIPELINES":{
    #         'data_spider.pipelines.AnimenewsnetworkDataPipeline':300,
    #     }
    # }

    def parse(self, response):
        """
        parse
        :param response: response object
        :return:
        """
        news_urls = response.xpath('//a[contains(@href,"/news/201")]/@href').getall()
        interest_urls = response.xpath('//a[contains(@href,"/interest/201")]/@href').getall()
        for news_url in news_urls:
            yield scrapy.Request(url=response.urljoin(news_url), callback=self.parse_news_interest)
        for interest_url in interest_urls:
            yield scrapy.Request(url=response.urljoin(interest_url), callback=self.parse_news_interest)
        for date in get_date_list():
            time_date = str(date).split()[0]
            yield scrapy.Request(url=self.ajax_url.format(day=time_date), callback=self.parse)

    def parse_news_interest(self, response):
        """
        parse_news_interest
        :param response: response object
        :return:
        """
        title = response.xpath("//title/text()").get()
        posted_at = response.xpath("//div[@id='page-title']//strong/text()").get()
        content = " ".join(response.xpath("//div[@class='meat']//text()").getall())
        content = filte(content)
        images_urls = response.xpath("//div[@class='meat']//img/@src").getall()
        video_urls = response.xpath('//p[@align="center"]//iframe/@src').get("")
        author = "".join(response.xpath('//div[@id="page-title"]/text()').getall())
        author = re.search(".*?by.*?(.*)\n", author).group(1)
        description = response.xpath('//meta[@name="description"]/@content').get("")
        url = response.url
        type = response.xpath("//div[@class='sub-title']/text()").get("")
        item = AnimenewsItem()
        item['title'] = title
        item['content'] = content
        item['images_urls'] = images_urls
        item['video_urls'] = video_urls
        item['description'] = description
        item['posted_at'] = posted_at
        item['author'] = author
        item['source_url'] = url
        item['type'] = type
        item['crawl_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        yield item
