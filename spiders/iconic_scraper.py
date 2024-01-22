import scrapy
import xml.etree.ElementTree as ET
from ..items import FashionbrandsItem
from scrapy.loader import ItemLoader
import json
import pandas as pd
class IconicSpider(scrapy.Spider):
    name = 'iconic__scraper'
    custom_settings = {
        'FEEDS': {f'./data/iconic_data.csv': {'format': 'csv', 'overwrite': True}}
    }
    def start_requests(self):
        df = pd.read_csv("./urls/iconic_urls.csv")
        for i in range(len(df)):
            url = df.loc[i,'url']
            yield scrapy.Request(url=url,callback=self.parse_product) 
    
    def parse_product(self, response):
        loader = ItemLoader(item=FashionbrandsItem(), response=response, selector=response)

        try:
            product_info_str = response.xpath("//script[2][@type='application/ld+json']/text()").get()
            product_info = json.loads(product_info_str)
        except:
            product_info = {}
        if product_info == {}:
            loader.add_value('in_stock', 'No')
            loader.add_value('url', response.request.url)
        else:
            product_name = product_info.get('name')
            loader.add_value('product_name', product_name)
            url = product_info.get('url')
            loader.add_value('url', url)
            loader.add_value('reference_url', url)
            imag = product_info.get('image')
            loader.add_value('product_image_url', imag)
            description = product_info.get('description')
            loader.add_value('description', description)
            sku = product_info.get('sku')
            loader.add_value('sku', sku)
            product_id = product_info.get('sku')
            loader.add_value('product_id', product_id)
            offers = product_info.get('offers')[0]
            price = offers.get('price')
            loader.add_value('price',price)
            price_currency = offers.get('priceCurrency')
            loader.add_value('price_currency', price_currency)
          
            out_stock = offers.get('availability') == 'http://schema.org/InStock'
            if out_stock:
                loader.add_value('in_stock', 'Yes')
            else:
                loader.add_value('in_stock', 'No')
            sizes = ','.join(response.xpath("//select[@id='SingleOptionSelector-0']/option/text()").getall())
            loader.add_value('sizes', sizes)
            loader.add_value('gender','Female')
            loader.add_value('brand_name', 'Iconic Boutique')
            loader.add_value('brand_logo', 'https://iconictheboutique.com/cdn/shop/files/iconic1_finalcroped_2068x.jpg?v=1613687516')
            yield loader.load_item()