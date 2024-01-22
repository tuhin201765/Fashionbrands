import scrapy
import xml.etree.ElementTree as ET
from ..items import ProductURL
from scrapy.loader import ItemLoader
import json

class PrbaSpider(scrapy.Spider):
    name = 'prba_spider'
    custom_settings = {
        'FEEDS': {f"{name.split('_')[0]}_urls.csv": {'format': 'csv', 'overwrite': True}}
    }
    def start_requests(self):
        yield scrapy.Request(url='https://oldnavy.gap.com/shop/th-sitemap-0.xml.gz', callback=self.parse)

    def parse(self, response):
        tree = ET.ElementTree(ET.fromstring(response.body))
        urls = tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
        urls = [url.text for url in urls]
        if 'https://www.portabellastores.com/collections/new' in urls:
            urls.remove('https://www.portabellastores.com/collections/new')
        for url in urls:
            yield scrapy.Request(url=url)
    
    def parse_cat(self, response):
        urls = response.xpath("//div[@class='css-0']/a/@href").getall()
        for url in urls:
            loader = ItemLoader(item=ProductURL())
            loader.add_value('url','https://www.portabellastores.com' + url)
            yield loader.load_item()
            
        next_page = response.xpath("//span[@class='next']/a/@href").get()
        if next_page:
            yield scrapy.Request(url='https://www.portabellastores.com' + next_page, callback=self.parse_cat)
    
    