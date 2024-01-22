import scrapy
import xml.etree.ElementTree as ET
from ..items import FashionbrandsItem
from scrapy.loader import ItemLoader
import json
import pandas as pd
class LuluSpider(scrapy.Spider):
    name = 'lulu_scraper'
    custom_settings = {
        'FEEDS': {f'./data/lulu_data.csv': {'format': 'csv', 'overwrite': True}}
    }
    def start_requests(self):
        df = pd.read_csv("./urls/lulu_urls.csv")
        for i in range(len(df)):
            url = df.loc[i,'url']
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
            price = response.xpath("//span[@class='price-1jnQj price']/span/text()").get()
            price = price.replace('$','')
            loader.add_value('price',price)
            loader.add_value('price_currency', 'USD')
            category = response.xpath("//li[@data-testid='breadcrumb-li'][1]/a/text()").get()
            loader.add_value('category', category)
            subcategory = response.xpath("//li[@data-testid='breadcrumb-li'][2]/a/text()").get()
            loader.add_value('category', subcategory)
            color = (',').join(response.xpath("//span[@class='colorSwatchImgWrapper-1k4IP']/picture/img/@alt").getall())
            loader.add_value('color', color)
            product_name = product_info.get('name')
            loader.add_value('product_name', product_name)
            description = product_info.get('description')
            loader.add_value('description', description)
            sku = product_info.get('sku')
            loader.add_value('sku', sku)
            product_id = product_info.get('sku')
            loader.add_value('product_id', product_id)
            imag = product_info.get('image')
            for img in imag:
                loader.add_value('product_image_url', img)
            offs = product_info.get('offers')
            out_stock = offs.get('availability') == 'InStock'
            if out_stock:
                loader.add_value('in_stock', 'Yes')
            else:
                loader.add_value('in_stock', 'No')
            url = offs.get('url')
            loader.add_value('url', url)
            loader.add_value('reference_url', url)
            loader.add_value('brand_name', 'lululemon')
            loader.add_value('brand_logo', 'https://cdn.cookielaw.org/logos/b5ce4b51-ea0c-47e5-b855-c12d511f57c9/18c69d7c-d4a2-4c41-9f9a-63346c1c395f/c3fe469e-0270-4eba-bc70-7fea061a6b35/lululemon_Yogo.jpg')
  
            yield loader.load_item()