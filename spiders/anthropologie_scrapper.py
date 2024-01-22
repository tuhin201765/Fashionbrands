import scrapy
import xml.etree.ElementTree as ET
from ..items import FashionbrandsItem
from scrapy.loader import ItemLoader
import json
import pandas as pd
class AnthropologieSpider(scrapy.Spider):
    name = 'anthropologie_scrapper'
    custom_settings = {
        'FEEDS': {f'prba_data.csv': {'format': 'csv', 'overwrite': True}}
    }
    def start_requests(self):
        df = pd.read_csv(f"{self.name.split('_')[0]}_urls.csv")
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

        product_name = product_info.get('name')
        if not product_name:
            product_name = response.xpath("//h1/text()").get()
        loader.add_value('product_name', product_name)

        gender = 'Male'
        loader.add_value('gender', gender)

        category = response.request.url.split('https://www.portabellastores.com/collections/')[-1].split('/')[0].strip()
        loader.add_value('category', category)

        subcategory = None
        loader.add_value('subcategory', subcategory)

        org_price = response.xpath("//span[@class='product__price product__price--compare']/text()").get()
        loader.add_value('orginal_price',org_price)

        price = response.xpath("//*[@class='product__price on-sale']/text()").get()
        if not price:
            price = response.xpath("//*[@class='product__price']/text()").get()
        loader.add_value('price', price)

        price_currency = 'USD'
        loader.add_value('price_currency', price_currency)

        sizes = ",".join(response.xpath("//input[@name='Size']/@value").getall())
        loader.add_value('sizes', sizes)

        description = product_info.get('description')
        if description == '' or description == None:
            description = "\n".join(response.xpath("//div[contains(@class,'description')][contains(@class,'product')]//text()").getall()).strip()
        loader.add_value('description', description)

        image = product_info.get('image')
        if image:
            image = image.get('url')
        loader.add_value('product_image_url', image)
        
        measurement = None
        loader.add_value('measurements', measurement)

        colors = ",".join(response.xpath("//input[@name='Color']/@value").getall())
        loader.add_value('color', colors)

        sku = product_info.get('sku')
        loader.add_value('sku', sku)
        if sku:
            product_id = sku
        else:
            product_id = response.request.url.split('/products/')[-1].split('?')[0].strip()

        loader.add_value('product_id', product_id)
        loader.add_value('url', response.request.url)
        loader.add_value('reference_url', response.request.url.split('/products/')[0])

        in_stock = response.xpath("//button[@name='add']/*[contains(text(),'Sold Out')]").get() == None
        if in_stock:
            loader.add_value('in_stock', 'Yes')
        else:
            loader.add_value('in_stock', 'No')
        yield loader.load_item()

