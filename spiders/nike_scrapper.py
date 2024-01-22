import scrapy
import xml.etree.ElementTree as ET
from ..items import FashionbrandsItem
from scrapy.loader import ItemLoader
import json
import pandas as pd
class NikeSpider(scrapy.Spider):
    name = 'nike_scraper'
    custom_settings = {
        'FEEDS': {f'./data/nike_data.csv': {'format': 'csv', 'overwrite': True}}
    }
    def start_requests(self):
        df = pd.read_csv("./urls/nike_urls.csv")
        for i in range(len(df)):
            url = df.loc[i,'url']
            yield scrapy.Request(url=url,callback=self.parse_product) 
    
    def parse_product(self, response):
        

        try:
            product_info_str = response.xpath("//script[@type='application/ld+json']/text()").get().strip()
            product_info = json.loads(product_info_str)
        except:
            product_info = {}

        category = response.xpath("//div[@class='pr2-sm css-1ou6bb2']/h2/text()").get()

        offers = product_info.get('offers')
        all_products = offers.get('offers')
        if all_products == None:
            print(offers)
            loader = ItemLoader(item=FashionbrandsItem(), response=response, selector=response)
            loader.add_value("brand_name",'Nike')
            loader.add_value("brand_logo","https://static.vecteezy.com/system/resources/thumbnails/010/994/412/small/nike-logo-black-with-name-clothes-design-icon-abstract-football-illustration-with-white-background-free-vector.jpg")
            loader.add_value('price_currency',offers.get('priceCurrency'))
            loader.add_value('price',offers.get('price'))
            loader.add_value('in_stock','No')
            description = response.xpath("//div[contains(@class,'description-preview')]//text()").getall()
            desc = "\n".join(description)
            loader.add_value("description",desc)

            loader.add_value('url',response.request.url)

            yield loader.load_item()
        else:
            for product in all_products:
                loader = ItemLoader(item=FashionbrandsItem(), response=response, selector=response)
                loader.add_value("product_id",product['itemOffered']['model'])
                loader.add_value("product_name",product['itemOffered']['name'])
                # loader.add_value("gender",)
                category = response.xpath("//*[@data-test='product-sub-title']/text()").get()
                loader.add_value("category",category)
                # loader.add_value("subcategory",)
                # loader.add_value("orginal_price",)
                loader.add_value("price",product['price'])
                loader.add_value("price_currency",product['priceCurrency'])
                loader.add_value("url",product['url'])
                # loader.add_value("reference_url",)
                # loader.add_value("sizes",)
                description = response.xpath("//div[contains(@class,'description-preview')]//text()").getall()
                desc = "\n".join(description)
                loader.add_value("description",desc)
                # loader.add_value("measurements",)
                loader.add_value("sku",product['itemOffered']['model'])
                loader.add_value("color",product['itemOffered']['color'])
                loader.add_value("product_image_url",product_info['image'])
                availability = product['availability']
                if availability == 'https://schema.org/InStock':
                    loader.add_value("in_stock",'Yes')
                else:
                    loader.add_value("in_stock",'No')
                loader.add_value("brand_name",'Nike')
                loader.add_value("brand_logo","https://static.vecteezy.com/system/resources/thumbnails/010/994/412/small/nike-logo-black-with-name-clothes-design-icon-abstract-football-illustration-with-white-background-free-vector.jpg")

                yield loader.load_item()
