import json
import math

import scrapy

from siteParser.items import ProductItem


class CatalogSpider(scrapy.Spider):
    name = 'catalog'
    allowed_domains = ['hobbygames.ru']
    start_urls = ['http://hobbygames.ru/catalog-all']
    pages_count = 313
    pg = 0

    def start_requests(self):
        for page in range(1, 1 + self.pages_count):
            url = f'https://hobbygames.ru/catalog-all?page={page}'
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_start_page(self, response, **kwargs):
        items = response.css('.catalog-info-count::text').extract_first('').strip()
        item_per_page = response.css('.limit .selected::text').extract_first('').strip()
        # self.pg = math.ceil(items / item_per_page)

    def parse_pages(self, response, **kwargs):
        for href in response.css('.product-item .name::attr("href")').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        item = ProductItem()
        item['url'] = response.request.url
        item['name'] = response.css('.product-info__main h1::text').extract_first('').strip()
        item['category'] = response.css('.product-types__type::text').extract_first('').strip()
        item['price'] = response.css('.price::text').extract_first('').strip()
        item['count_players'] = response.css('.players span::text').extract_first('').strip()
        item['time'] = response.css('.time span::text').extract_first('').strip()
        item['age'] = response.css('.age span::text').extract_first('').strip()
        description = response.css('.desc-text p::text').extract()
        description = [str(i.strip()) for i in description]
        item['description'] = " ".join(description)
        item['year'] = response.css('.manufacturers__value::text').extract_first('').strip()
        item['producer'] = response.css('.manufacturers__value::text').extract()[1].strip()

        yield item
