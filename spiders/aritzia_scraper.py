import scrapy
import xml.etree.ElementTree as ET
from ..items import FashionbrandsItem
from scrapy.loader import ItemLoader
import json
import pandas as pd
class AritziaSpider(scrapy.Spider):
    name = 'aritzia_scraper'
    custom_settings = {
        'FEEDS': {f'./data/aritzia_data.csv': {'format': 'csv', 'overwrite': True}}
    }
    def start_requests(self):
        df = pd.read_csv("./urls/aritzia_urls.csv")
        for i in range(len(df)):
            url = df.loc[i,'url']
            url = url.replace('/fr/','/us/')+ '?country=us'
            yield scrapy.Request(url=url,callback=self.parse_product) 
        
    
    def parse_product(self, response):
        loader = ItemLoader(item=FashionbrandsItem(), response=response, selector=response)

        try:
            product_info_str = response.xpath("//script[@type='application/ld+json'][1]/text()").get()
            product_info = json.loads(product_info_str)
        except:
            product_info = {}
        if product_info == {}:
            loader.add_value('in_stock', 'No')
            loader.add_value('url', response.request.url)
        else:
            category = product_info.get('itemListElement')[0].get('item').get('name')
            loader.add_value('category', category)
            subcategory = product_info.get('itemListElement')[1].get('item').get('name')
            loader.add_value('subcategory', subcategory)
            
            of = response.xpath("//script[@type='application/ld+json']/text()").getall()[-1]
            offers = json.loads(of)
            product_name = offers.get('name')
            loader.add_value('product_name', product_name)
            description = offers.get('description')
            loader.add_value('description', description)
            sku = offers.get('sku')
            loader.add_value('sku', sku)
            product_id = offers.get('mpn')
            loader.add_value('product_id', product_id)
            imag = offers.get('image')
            for img in imag:
                loader.add_value('product_image_url', img)
            loader.add_value('brand_name', 'Aritzia')
            loader.add_value('brand_logo', 'https://www.aritzia.com/on/demandware.static/Sites-Aritzia_INTL-Site/-/default/dw3be993fe/images/aritzia_skin/aritzia_logo.svg')

            offs = offers.get('offers')
            price = offs.get('price')
            loader.add_value('price',price)
            price_currency = offs.get('priceCurrency')
            loader.add_value('price_currency', price_currency)
            out_stock = offs.get('availability') == 'http://schema.org/InStock'
            if out_stock:
                loader.add_value('in_stock', 'Yes')
            else:
                loader.add_value('in_stock', 'No')
            yield loader.load_item()

            measurement = None
            loader.add_value('measurements', measurement)
            url = offs.get('url')
            loader.add_value('url', url)
            loader.add_value('reference_url', url)

        
            yield loader.load_item()