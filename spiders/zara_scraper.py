import scrapy
import pandas as pd
import json
class ZaraScraperSpider(scrapy.Spider):
    name = 'zara_scraper'
    custom_settings = {
        'FEEDS': {f'zara_data.csv': {'format': 'csv', 'overwrite': True}}
    }
    def start_requests(self):
        df = pd.read_csv(f"{self.name.split('_')[0]}_urls.csv")
        df = df[0:1]
        for i in range(len(df)):
            url = df.loc[i,'url']
            meta = df.loc[i,'meta']


            data = eval(meta)
            data = data[0]
            meta_data = dict()
            meta_data['product_id'] = data['id']
            meta_data['product_name'] = data['name']
            meta_data['description'] = data['description']
            meta_data['price'] = float(data['price'])/100

            details = data.get('detail')
            
            color_names = None
            if details:
                colors = details.get('colors')
                if colors:
                    
                    color_names = [color['name'] for color in colors]

            if details:
                colors = details.get('colors')
                if colors:
                    xmedia = colors[0]['xmedia']
                    if xmedia:
                        try:
                            meta_data['product_image_url'] = 'https://static.zara.net/photos' + xmedia[0]['path'] + '/' + xmedia[0]['name'] + '.jpg?ts=' +  xmedia[0]['timestamp']
                        except:
                            pass
            meta_data['color'] = ",".join(color_names)
            meta_data['category'] = data['category']
            if meta_data['category'].lower() == 'man':
                meta_data['gender'] = 'MEN'
            elif meta_data['category'].lower() == 'woman':
                meta_data['gender'] = 'WOMEN'
            meta_data['subcategory'] = data['subcategory']

            meta_data['price_currency'] = 'USD'
            meta_data['url'] = url
            meta_data['in_stock'] = data['availability']
            yield scrapy.Request(url=url,callback=self.parse_product,cb_kwargs={'meta_data':meta_data}) 

    def parse_product(self, response,meta_data):
        sizes = ",".join(response.xpath("//span[@class='product-size-info__main-label']/text()").getall())
        meta_data['sizes'] = sizes
        script = response.xpath("//div[@id='app-root']/following::script[@data-compress]").get()  
        store_id = script.split('storeId')[1].split(':')[1].split(',')[0]
        product_id = response.request.url.split('v1=')[-1].strip()
        measure_url = f"https://www.zara.com/itxrest/1/catalog/store/{store_id}/product/{product_id}/size-measure-guide?locale=en_US"
        # print(meta_data)
        yield scrapy.Request(url=measure_url, callback=self.parse_measure,cb_kwargs={'meta_data':meta_data})

    def parse_measure(self, response,meta_data):
        measure_info = []
        size_data = json.loads(response.body)
        sizeGuideInfo = size_data['sizeGuideInfo']
        sizes = sizeGuideInfo['sizes']
        for size in sizes:
            measure_dict = dict()
            measure_dict['size_name'] = size['name']
            measures = size['measures']
            all_measures = [m['dimensions'] for m in measures]
            measure_dict['measures'] = all_measures

            measure_info.append(measure_dict)
        meta_data['measure_info'] = measure_info
        print(meta_data)

