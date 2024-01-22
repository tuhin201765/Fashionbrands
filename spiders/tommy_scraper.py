import scrapy
import xml.etree.ElementTree as ET
from ..items import FashionbrandsItem
from scrapy.loader import ItemLoader
import json
import pandas as pd
class OldNavySpider(scrapy.Spider):
    name = 'tommy_scraper'
    custom_settings = {
        'FEEDS': {f'tommy_data.csv': {'format': 'csv', 'overwrite': True}}
    }
    def start_requests(self):
        df = pd.read_csv('tommy_urls.csv')
        # df = pd.read_csv(f"{self.name.split('_')[0]}_urls.csv")
        for i in range(len(df)):
            url = df.loc[i,'url']
            yield scrapy.Request(url=url,callback=self.parse_product) 
    
    def parse_product(self, response):
        loader = ItemLoader(item=FashionbrandsItem(), response=response, selector=response)

        try:
            product_info_str = response.xpath("//html/body/script[9]/text()").get().strip()
            product_info = json.loads(product_info_str)
        except:
            product_info = {}

        product_name = product_info.get('name')
        if not product_name:
            product_name = response.xpath("//h1/text()").get()
        loader.add_value('product_name', product_name)


        description = product_info.get('description')
        if description == '' or description == None:
            description = response.xpath("//span[@class='col-12 col-xl-8']/text()").get()
        loader.add_value('description', description)

        
        if description:
            gender = description[15:22]
            loader.add_value('gender', gender)
        else:
            loader.add_value('gender', '')
        

        # category = response.request.url.split('https://www.portabellastores.com/collections/')[-1].split('/')[0].strip()
        # loader.add_value('category', category)

        subcategory = None
        loader.add_value('subcategory', subcategory)

        org_price = response.xpath("//span[@class='strike-through list']/span/text()").get()
        loader.add_value('orginal_price',org_price)

        # price = response.xpath("//*[@class='product__price on-sale']/text()").get()
        price = response.xpath("//span[@class='sales body-font md']/span/text()").get()
        loader.add_value('price', price)

        price_currency = 'USD'
        loader.add_value('price_currency', price_currency)

        sizes = response.xpath("//ul[@class='variant-list']/label/text()").get()
        loader.add_value('sizes', sizes)



        # image = product_info.get('image')
        # if image:
        #     image = image.get('url')
        # else:
        image = ",".join(response.xpath("//div[@class='product-images__wrapper ']/div/div/img/@src").getall())
        loader.add_value('product_image_url', image)
        
        measurement = None
        loader.add_value('measurements', measurement)

        colors = ",".join(response.xpath("//ul[@class='variant-list']/li/label/span[2]/text()").getall())
        loader.add_value('color', colors)

        sku = response.xpath("//span[@class='productsku']/text()").get()
        loader.add_value('sku', sku)
        # if sku:
        #     product_id = sku
        # else:
        product_id = response.xpath("//div[@class='product-number d-none']/span/text()").get()

        loader.add_value('product_id', product_id)
        loader.add_value('url', response.request.url)
        loader.add_value('reference_url', response.request.url.split('/products/')[0])

        in_stock = response.xpath("//div[@class='product-details--desk']/div/div/*[contains(text(),'Sold Out')]").get()
        if in_stock and prod:
            loader.add_value('in_stock', 'No')
        else:
            loader.add_value('in_stock', 'Yes')
        yield loader.load_item()