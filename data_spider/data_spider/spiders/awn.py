import scrapy
import re
import time
import logging
from data_spider.utils.get_date import get_date_list
from data_spider.utils.filter_html import filte
from data_spider.utils.switch_date import switch_time
from data_spider.items import AwnItem

class AwnSpider(scrapy.Spider):
    name = 'awn'
    allowed_domains = ['awn.com']
    blog_start_urls = "https://www.awn.com/blog?page={page}"
    news_start_urls = "https://www.awn.com/news?page={page}"
    logger = logging.getLogger(__name__)

    def start_requests(self):
        for news_page in range(1,1997):
            yield scrapy.Request(url=self.news_start_urls.format(page=news_page), callback=self.parse)
        for blog_page in range(1,228):
            yield scrapy.Request(url=self.blog_start_urls.format(page=blog_page), callback=self.parse)

    def parse(self, response):
        detail_urls = response.xpath("//span[@class='title-with-tag']/a/@href").getall()
        detail_urls = list(map(lambda url:response.urljoin(url),detail_urls))
        for detail_url in detail_urls:
            yield scrapy.Request(url=detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        try:
            spider_name = self.name
            content = filte("".join(response.xpath("//div[@class='field-items']/div[@class='field-item even']//text()").getall()))
            images_urls = response.xpath("//div[@class='field-items']//img/@src").getall()
            video_urls = response.xpath("//div[@class='field-items']//iframe/@src").getall()
            description = response.xpath("//meta[@name='description']/@content").get()
            posted_at = response.xpath("//footer[@class='submitted']//text()").getall()[2]
            posted_at = re.findall(r"\|.*?,(.*?)at.*?",posted_at)[0].strip()
            # posted_at = re.findall(r"(.*?)(\d){1,2},(\d+),.*?", posted_at)
            month, day, year = re.findall(r"(.*?)\s+(\d+){1,2},\s+(\d+)", posted_at)[0]
            posted_at = switch_time(month, day, year)
            author = response.xpath("//a[@class='username']/text()").get()
            crawl_time = time.strftime("%Y-%m-%d", time.localtime())
            source_url = response.url
            title = response.xpath("//h1[@id='page-title']//text()").get().strip()
            tags = ",".join(response.xpath("//div[@class='field-items']//div//a//text()").getall())

            item = AwnItem(spider_name=spider_name, content=content, images_urls=images_urls, video_urls=video_urls,
                               description=description, posted_at=posted_at, author=author, source_url=source_url,
                               title=title, tags=tags, crawl_time=crawl_time)
            yield item
        except Exception as e:
            self.logger.debug("Exception:%s" %(e.args))
