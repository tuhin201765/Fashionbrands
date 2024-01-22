import scrapy
import xml.etree.ElementTree as ET
from ..items import ProductURL
from scrapy.loader import ItemLoader

class HMSpider(scrapy.Spider):
    name = 'hm__spider'
    custom_settings = {
        'FEEDS': {f"./urls/{name.split('_')[0]}_urls.csv": {'format': 'csv', 'overwrite': True}}
    }
    def start_requests(self):
        yield scrapy.Request(url='https://www2.hm.com/en_us.sitemap.xml', callback=self.parse, dont_filter=True)
    def parse(self, response):
        tree = ET.ElementTree(ET.fromstring(response.body))
        urls = tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
        urls = [url.text for url in urls]
        for url in urls[73:]:
            yield scrapy.Request(url=url,callback=self.parse_cat)
            # loader = ItemLoader(item=ProductURL())
            # loader.add_value('url', url)
            # yield loader.load_item()

    def parse_cat(self, response):
        tree = ET.ElementTree(ET.fromstring(response.body))
        urls = tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
        urls = [url.text for url in urls]
        for url in urls:
            loader = ItemLoader(item=ProductURL())
            loader.add_value('url', url)
            yield loader.load_item()