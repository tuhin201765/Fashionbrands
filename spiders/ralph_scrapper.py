import scrapy
import xml.etree.ElementTree as ET
from ..items import FashionbrandsItem
from scrapy.loader import ItemLoader
import json
import pandas as pd
class RalphSpider(scrapy.Spider):
    name = 'ralph_scrapper'
    custom_settings = {
        'FEEDS': {f'ralph_data.csv': {'format': 'csv', 'overwrite': True}}
    }
    def start_requests(self):
        df = pd.read_csv("ralph_urls.csv")
        for i in range(len(df)):
            url = df.loc[i,'url']
            yield scrapy.Request(url=url,callback=self.parse_product) 
    
    def parse_product(self, response):
        loader = ItemLoader(item=FashionbrandsItem(), response=response, selector=response)

        try:
            product_info_str = response.xpath("//div[@id='wrapper']/script[1]/text()").get().strip()
            data = product_info_str.split('\nvar digitalData = \'\';\nfunction init() {\ndigitalData = ')[-1].split(';\nwindow.addEventListener')[0]

            jsons = data.get('product')
            item = jsons.get('item')[0]
            product_info = json.loads(item)

            
        except:
            product_info = {}
            product_name = product_info.get('productName')

            loader.add_value('product_name', product_name)

            gender = product_info.get("productDivision")
            loader.add_value('gender', gender)

            category = product_info.get("productWebCategory")
            loader.add_value('category', category)

            org_price = product_info.get("productPrice")
            loader.add_value('orginal_price',org_price)

            price = product_info.get("productOriginalPrice")
            loader.add_value('price', price)

            price_currency = 'USD'
            loader.add_value('price_currency', price_currency)

            description = product_info.get('productLongDescription')
            loader.add_value('description', description)

            image = response.xpath("//div[@class='product-primary-image dfrefreshcont']/div/div/div[1]/div/picture/img/@src").get()

            loader.add_value('product_image_url', image)
    
            product_id = product_info.get("productID")

            loader.add_value('product_id', product_id)
            loader.add_value('url', response.request.url)
            loader.add_value('reference_url', response.request.url.split('/products/')[0])

            out_stock = product_info.get("productStockMessage")
            loader.add_value('in_stock', out_stock)
            yield loader.load_item()
