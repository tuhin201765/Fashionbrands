import scrapy
import json
from ..items import ProductURL
from scrapy.loader import ItemLoader

class ZaraSpiderSpider(scrapy.Spider):
    name = 'zara_spider'
    custom_settings = {
        'FEEDS': {f"{name.split('_')[0]}_urls.csv": {'format': 'csv', 'overwrite': True}}
    }

    def start_requests(self):
        yield scrapy.Request(url='https://www.zara.com/us/en/categories?ajax=true', callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)
        cats = data['categories']
        for cat in cats:
            subcats = cat['subcategories']
            for subcat in subcats:
                subcat_info = None

                # Need to be in recursive loop
                all_items = []
                def get_product(sc):
                    if sc['subcategories'] == []:
                        subcat_info = {'cat':sc['sectionName'],'subcat':sc['name'],'url':f"https://www.zara.com/us/en/category/{sc['id']}/products?ajax=true"}
                        all_items.append(subcat_info)
                    else:
                        for s in sc['subcategories']:
                            get_product(s)
                
                get_product(subcat)

                for subcat_info in all_items:
                    yield scrapy.Request(url=subcat_info['url'], meta=subcat_info, callback=self.parse_products)
                # if subcat['subcategories'] == []:
                #     subcat_info = {'cat':subcat['sectionName'],'subcat':subcat['name'],'url':f"https://www.zara.com/us/en/category/{subcat['id']}/products?ajax=true"}
                # else:
                #     subsubcats = subcat['subcategories']
                #     for subsubcat in subsubcats:
                #         if subsubcat['subcategories'] == []:
                #             subcat_info = {'cat':subcat['sectionName'],'subcat':subsubcat['name'],'url':f"https://www.zara.com/us/en/category/{subsubcat['id']}/products?ajax=true"}
                #         else:
                #             subsubsubcats = subsubcat['subcategories']
                #             for subsubsubcat in subsubsubcats:
                #                 subcat_info = {'cat':subcat['sectionName'],'subcat':subsubsubcat['name'],'url':f"https://www.zara.com/us/en/category/{subsubsubcat['id']}/products?ajax=true"}
                # if subcat_info:
                    
                

    def parse_products(self, response):
        data = json.loads(response.body)
        # try:
        #     data['productGroups'][0].keys()
        # except:
        #     print(response.request.url)
        #     input()
        product_groups = data['productGroups']
        for product_group in product_groups:
            items = product_group['elements']
            for item in items:
                products = item.get('commercialComponents')
                if products:
                    for product in products:
                        if product['id'] != 'seo-info':
                            url = "https://www.zara.com/us/en/" + product['seo']['keyword'] + '-p' +  product['seo']['seoProductId'] + '.html'
                            try:
                                url = url + '?v1=' + str(product['seo']['discernProductId'])
                            except:
                                pass
                            meta = product
                            meta['category'] = response.request.meta['cat']
                            meta['subcategory'] = response.request.meta['subcat']

                            loader = ItemLoader(item=ProductURL())
                            loader.add_value('url',url)
                            loader.add_value('meta',json.dumps(meta))
                            yield loader.load_item()

