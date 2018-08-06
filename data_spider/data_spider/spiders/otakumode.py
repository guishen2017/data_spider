# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from data_spider.items import OtakumodeItem
from data_spider.utils.filter_html import filte


class OtakumodeSpider(CrawlSpider):
    name = 'otakumode'
    allowed_domains = ['otakumode.com']
    start_urls = ['https://otakumode.com/news']
    rules = (
        Rule(LinkExtractor(allow=r'.*?/news/.*/'), callback='parse_news', follow=True),
    )
    def parse_news(self, response):
        """
        parse news
        :param response:response object
        :return:
        """
        title = response.xpath("//div[@class='c-docs--single-column']/h1"
                               "[@class='p-article__title']/text()").get()
        content = "".join(response.xpath("//div[@class='p-ar"
                                         "ticle__body c-docs--normalize']//text()").getall())
        content = filte(content)
        images_urls = response.xpath("//div[@class='p-artic"
                                     "le__body c-docs--normalize']//img/@src").getall()
        header_image_url = response.xpath('//div[@class="p-article__figure-inner"]/img/@src').get()
        images_urls.append(header_image_url)
        video_urls = response.xpath('//div[@class="p-article__fi'
                                    'gure-inner"]//iframe[@src]/@src').getall()
        description = response.xpath('//meta[@name="description"]/@content').get()
        posted_at = response.xpath('//time[@class="p-article__time"]/@datetime').get()
        crawl_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        source_url = response.url
        anime_type = response.xpath('//ul[@class="list--inline u-float-left"]/li/a'
                                    '[@class="p-article__category"]/text()').get()
        tags = ",".join(response.xpath('//a[@class="c-btn c-bt'
                                       'n--sm c-btn--icon-left c-btn--tag"]//text()').getall())
        item = OtakumodeItem()
        item['title'] = title
        item['content'] = content
        item['images_urls'] = images_urls
        item['video_urls'] = video_urls
        item['description'] = description
        item['posted_at'] = posted_at
        item['crawl_time'] = crawl_time
        item['source_url'] = source_url
        item['type'] = anime_type
        item['tags'] = tags
        yield item

