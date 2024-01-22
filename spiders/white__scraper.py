import scrapy
import xml.etree.ElementTree as ET
from ..items import FashionbrandsItem
from scrapy.loader import ItemLoader
import json
import pandas as pd
from bs4 import BeautifulSoup as bs

class WhiteSpider(scrapy.Spider):
    name = 'white__scrapper'
    custom_settings = {
        'FEEDS': {f'./data/white_data.csv': {'format': 'csv', 'overwrite': True}}
    }
    def start_requests(self):
        df = pd.read_csv("./urls/white_urls.csv")
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
            so = product_info.get('description')
            soup = bs(so, 'html.parser').get_text()
            loader.add_value('description', soup)
            url = product_info.get('url')
            loader.add_value('url', url)
            price = product_info.get('Offers')[0].get('price')
            loader.add_value('price', price)
            loader.add_value('price_currency', 'USD')
            product_name = response.xpath("//h1[@class='product-name']/text()").get()
            loader.add_value('product_name', product_name)
            # product_name =product_info.get('name')
            image = 'https://www.whitehouseblackmarket.com'+ product_info.get('image')
            loader.add_value('product_image_url', image)
            product_id = url.split('/')[-1]
            loader.add_value('product_id', product_id)
            sku = url.split('/')[-1]
            of = product_info.get('Offers')
            for o in of:
                colors = o.get('itemOffered').get('color')
                loader.add_value('color', colors)
                out_stock = o.get('availability') == 'http://schema.org/InStock'
                if out_stock:
                    loader.add_value('in_stock', 'Yes')
                else:
                    loader.add_value('in_stock', 'No')
                yield loader.load_item()

            loader.add_value('sku', sku)
            loader.add_value('brand_name', 'White House Black Market')
            loader.add_value('brand_logo', 'https://mma.prnewswire.com/media/1244821/White_House_Black_Market_Logo.jpg?p=facebook')
            loader.add_value('gender', 'Woman')
            loader.add_value('reference_url', url)
        
            yield loader.load_item()