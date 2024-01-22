import scrapy
import xml.etree.ElementTree as ET
from ..items import FashionbrandsItem
from scrapy.loader import ItemLoader
import json
import pandas as pd
class BananaSpider(scrapy.Spider):
    name = 'banana__scraper'
    custom_settings = {
        'FEEDS': {f'./data/banana_data.csv': {'format': 'csv', 'overwrite': True}}
    }
    def start_requests(self):
        df = pd.read_csv("banana_urls.csv")
        for i in range(len(df)):
            url = df.loc[i,'url']
            yield scrapy.Request(url=url,callback=self.parse_product) 
    
    def parse_product(self, response):
        loader = ItemLoader(item=FashionbrandsItem(), response=response, selector=response)

        try:
            product_info_str = response.xpath("//script[@type='application/ld+json']/text()").get().strip()
            product_info = json.loads(product_info_str)
        except:
            product_info = {}
        if product_info_str == None:
            loader.add_value('in_stock', 'No')
            loader.add_value('url', response.request.url)
        else:
            pro = product_info[0]
            pros = product_info[1]
            gender = pros.get('itemListElement')[0].get('item').get('name')
            loader.add_value('gender', gender)
            category = pros.get('itemListElement')[1].get('item').get('name')
            loader.add_value('category', category)
            offer = pro.get('offers')[0]
            product_name = offer.get('itemOffered').get('name')
            loader.add_value('product_name', product_name)
            image = offer.get('itemOffered').get('image')
            loader.add_value('product_image_url', image)
            product_id = offer.get('itemOffered').get('sku')
            loader.add_value('product_id', product_id)
            sku = offer.get('itemOffered').get('sku')
            loader.add_value('sku', sku)
            description = offer.get('itemOffered').get('description')
            loader.add_value('description', description)
            price = offer.get('price')
            loader.add_value('price', price)
           
            colors = offer.get('itemOffered').get('color')
            loader.add_value('color', colors)
            price_currency = offer.get('priceCurrency')
            loader.add_value('price_currency', price_currency)
            url = offer.get('url')
            loader.add_value('url', url)
            out_stock = offer.get('availability') == 'https://schema.org/InStock'
            if out_stock:
                loader.add_value('in_stock', 'Yes')
            else:
                loader.add_value('in_stock', 'No')
            loader.add_value('brand_name','BANANA REPUBLIC')
            loader.add_value('brand_logo','https://bananarepublic.gap.com/Asset_Archive/BRWeb/content/0016/264/099/assets/BR_Logo_black.svg')

            loader.add_value('url', response.request.url)
            loader.add_value('reference_url', response.request.url)
            yield loader.load_item()