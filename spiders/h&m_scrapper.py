import scrapy
import xml.etree.ElementTree as ET
from ..items import FashionbrandsItem
from scrapy.loader import ItemLoader
import json
import pandas as pd
class HMSpider(scrapy.Spider):
    name = 'hm__scrapper'
    custom_settings = {
        'FEEDS': {f'./data/hm_data.csv': {'format': 'csv', 'overwrite': True}}
    }
    def start_requests(self):
        df = pd.read_csv("./urls/hm_urls.csv")
        for i in range(len(df)):
            url = df.loc[i,'url']
            yield scrapy.Request(url=url,callback=self.parse_product) 
    
    def parse_product(self, response):
        loader = ItemLoader(item=FashionbrandsItem(), response=response, selector=response)

        try:
            product_info_str = response.xpath("//script[@type='application/ld+json'][1]/text()").get().strip()
            product_info = json.loads(product_info_str)
        except:
            product_info = {}
        if product_info == {}:
            loader.add_value('in_stock', 'No')
            loader.add_value('url', response.request.url)
        else:
            # pro = product_info[0]
            # pros = product_info[1]
            gender = product_info.get('itemListElement')[1].get('name')
            loader.add_value('gender', gender)
            category = product_info.get('itemListElement')[2].get('name')
            loader.add_value('category', category)
            subcategory = product_info.get('itemListElement')[3].get('name')
            loader.add_value('subcategory', subcategory)


            of = response.xpath("//script[@type='application/ld+json'][2]/text()").get().strip()
            offer = json.loads(of)

            product_name = offer.get('name')
            loader.add_value('product_name', product_name)
            image = offer.get('image')
            loader.add_value('product_image_url', image)

            product_id = offer.get('sku')
            loader.add_value('product_id', product_id)

            sku = offer.get('sku')
            loader.add_value('sku', sku)
            description = offer.get('description')
            loader.add_value('description', description)
            colors = offer.get('color')
            loader.add_value('color', colors)

            offers = offer.get('offers')[0]

            price = offers.get('price')
            loader.add_value('price', price)
            
            price_currency = offers.get('priceCurrency')
            loader.add_value('price_currency', price_currency)
            url = offers.get('url')
            loader.add_value('url', url)
            out_stock = offers.get('availability') == 'http://schema.org/InStock'
            if out_stock:
                loader.add_value('in_stock', 'Yes')
            else:
                loader.add_value('in_stock', 'No')
            # yield loader.load_item()

            loader.add_value('url', response.request.url)
            loader.add_value('reference_url', response.request.url)
            yield loader.load_item()