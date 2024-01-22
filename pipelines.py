# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
from .items import FashionbrandsItem,ProductURL
class fashionbrandsPipeline:
    def process_item(self, item, spider):
        return item

class DefaultValuesPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, FashionbrandsItem):
            item.setdefault('product_id', '')
            item.setdefault("product_name","")
            item.setdefault("gender","")
            item.setdefault("category","")
            item.setdefault("subcategory","")
            item.setdefault("orginal_price","")
            item.setdefault("price","")
            item.setdefault("price_currency","")
            item.setdefault("scraped_time",datetime.today().strftime('%Y-%m-%d'))
            item.setdefault("url","")
            item.setdefault("reference_url","")
            item.setdefault("sizes","")
            item.setdefault("description","")
            item.setdefault("measurements","")
            item.setdefault("sku","")
            item.setdefault("color","")
            item.setdefault("product_image_url","")
            item.setdefault("scraped_time","")
            item.setdefault("in_stock","")
        elif isinstance(item, ProductURL):
            item.setdefault('url', '')
            item.setdefault('meta', '')

        return item
