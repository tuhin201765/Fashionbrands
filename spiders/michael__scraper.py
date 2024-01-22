import scrapy
import xml.etree.ElementTree as ET
from ..items import FashionbrandsItem
from scrapy.loader import ItemLoader
import json
import pandas as pd
class MichaelSpider(scrapy.Spider):
    name = 'michael_scraper'
    custom_settings = {
        'FEEDS': {f'./data/michael_data.csv': {'format': 'csv', 'overwrite': True}}
    }
    def start_requests(self):
        df = pd.read_csv("./urls/michael_urls.csv")
        for i in range(len(df)):
            url = df.loc[i,'url']
            yield scrapy.Request(url=url,callback=self.parse_product) 
    
    def parse_product(self, response):
        loader = ItemLoader(item=FashionbrandsItem(), response=response, selector=response)

        try:
            product_info_str = response.xpath("//script[@type='application/ld+json'][2]/text()").get().strip()
            product_info = json.loads(product_info_str)
        except:
            product_info = {}
        if product_info == {}:
            loader.add_value('in_stock', 'No')
            loader.add_value('url', response.request.url)
        else:
            
            pro = response.xpath("//script[@type='application/ld+json'][1]/text()").get().strip()
            pros = json.loads(pro)
            category = pros.get('itemListElement')[1].get('item').get('name')
            loader.add_value('category', category)
            subcategory = pros.get('itemListElement')[2].get('item').get('name')
            loader.add_value('category', subcategory)
            loader.add_value('category', 'Female')
            offers = product_info.get('@graph')
        for offer in offers:
            product_name = offer.get('name')
            loader.add_value('product_name', product_name)
            so = offer.get('description')
            loader.add_value('description', so)
            image = offer.get('image')
            loader.add_value('product_image_url', image)
            colors = offer.get('color')
            loader.add_value('color', colors)
            sku = offer.get('sku')
            loader.add_value('sku', sku)
            product_id = offer.get('productID')
            loader.add_value('product_id', product_id)

            price = offer.get('offers').get('price')
            loader.add_value('price', price)
            price_currency = offer.get('offers').get('priceCurrency')
            loader.add_value('price_currency', price_currency)


            out_stock = offer.get('offers').get('availability') == 'https://schema.org/InStock'
            if out_stock:
                loader.add_value('in_stock', 'Yes')
            else:
                loader.add_value('in_stock', 'No')
            yield loader.load_item()

            measurement = None
            loader.add_value('measurements', measurement)
            loader.add_value('url', response.request.url)
            loader.add_value('reference_url', response.request.url)
            loader.add_value('brand_name', 'MICHAEL Michael Kors')
            loader.add_value('brand_logo', 'https://www.michaelkors.com/img/logo_mk.webp')

        
            yield loader.load_item()



