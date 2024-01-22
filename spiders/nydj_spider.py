import scrapy
import xml.etree.ElementTree as ET
from ..items import ProductURL
from scrapy.loader import ItemLoader

class NydjSpider(scrapy.Spider):
    name = 'nydj_spider'
    custom_settings = {
        'FEEDS': {f"./urls/{name.split('_')[0]}_urls.csv": {'format': 'csv', 'overwrite': True}}
    }
    def start_requests(self):
        yield scrapy.Request(url='https://nydj.com/sitemap_products_1.xml?from=5173336834093&to=7460216569901', callback=self.parse, dont_filter=True)

    def parse(self, response):
        tree = ET.ElementTree(ET.fromstring(response.body))
        urls = tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
        urls = [url.text for url in urls]
        for url in urls:
            loader = ItemLoader(item=ProductURL())
            loader.add_value('url', url)
            yield loader.load_item()