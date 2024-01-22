# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from itemloaders.processors import TakeFirst,MapCompose,Compose
import scrapy

def parse_string(s):
    if(s):
        s1 = "".join(s)
        return s1.strip()
    else:
        return 

def parse_price(s):
    return float(s[0])
class FashionbrandsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field(output_processor=TakeFirst(),input_processor=Compose(parse_desc))
    product_id = scrapy.Field(output_processor=TakeFirst(),input_processor=Compose(parse_string))
    product_name = scrapy.Field(output_processor=TakeFirst(),input_processor=Compose(parse_string))
    gender = scrapy.Field(output_processor=TakeFirst(),input_processor=Compose(parse_string))
    category = scrapy.Field(output_processor=TakeFirst(),input_processor=Compose(parse_string))
    subcategory = scrapy.Field(output_processor=TakeFirst(),input_processor=Compose(parse_string))
    orginal_price = scrapy.Field(output_processor=TakeFirst(),input_processor=Compose(parse_price ))
    price = scrapy.Field(output_processor=TakeFirst(),input_processor=Compose(parse_price))
    price_currency = scrapy.Field(output_processor=TakeFirst(),input_processor=Compose(parse_string))
    url = scrapy.Field(output_processor=TakeFirst(),input_processor=Compose(parse_string))
    reference_url = scrapy.Field(output_processor=TakeFirst(),input_processor=Compose(parse_string))
    sizes = scrapy.Field(output_processor=TakeFirst(),input_processor=Compose(parse_string))
    description = scrapy.Field(output_processor=TakeFirst(),input_processor=Compose(parse_string))
    measurements = scrapy.Field(output_processor=TakeFirst(),input_processor=Compose(parse_string))
    sku = scrapy.Field(output_processor=TakeFirst(),input_processor=Compose(parse_string))	
    color = scrapy.Field(output_processor=TakeFirst(),input_processor=Compose(parse_string))
    product_image_url = scrapy.Field(output_processor=TakeFirst(),input_processor=Compose(parse_string))
    in_stock = scrapy.Field(output_processor=TakeFirst(),input_processor=Compose(parse_string))
    scraped_time  = scrapy.Field(output_processor=TakeFirst(),input_processor=Compose(parse_string))
    brand_name = scrapy.Field(output_processor=TakeFirst(),input_processor=Compose(parse_string))
    brand_logo = scrapy.Field(output_processor=TakeFirst(),input_processor=Compose(parse_string))

class ProductURL(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst(),input_processor=Compose(parse_string))
    meta = scrapy.Field()