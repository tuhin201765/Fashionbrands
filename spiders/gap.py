import scrapy
import xml.etree.ElementTree as ET
from ..items import ProductURL
from scrapy.loader import ItemLoader

class GapSpider(scrapy.Spider):
    name = 'gap'
    custom_settings = {
        'FEEDS': {f"{name.split('_')[0]}_urls.csv": {'format': 'csv', 'overwrite': True}}
    }
    def start_requests(self):
        yield scrapy.Request(url='https://www.gap.com/native-product-sitemap.xml', callback=self.parse, dont_filter=True)
    def parse(self, response):
        tree = ET.ElementTree(ET.fromstring(response.body))
        urls = tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
        urls = [url.text for url in urls]
        for url in urls:
            # yield scrapy.Request(url=url,callback=self.parse_cat)
            loader = ItemLoader(item=ProductURL())
            loader.add_value('url', url)
            yield loader.load_item()