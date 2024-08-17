import scrapy
import xmltodict
import json
import datetime
import csv
import os

date = datetime.datetime.today().strftime('%m_%d_%y')

class EthncSpider(scrapy.Spider):
    name = "ethnc"
    allowed_domains = ["ethnc.com"]
    start_urls = ["https://pk.ethnc.com/sitemap_collections_1.xml"]

    if f"ethnc_{date}.csv" not in os.listdir(os.getcwd()):
        with open(f"ethnc_{date}.csv","a",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(['date','link','category','title','old_price','new_price','option','quantity'])

    custom_settings = {
        "DOWNLOAD_DELAY":1
    }

    def parse(self, response):
        links = [i['loc'] for i in xmltodict.parse(response.text)['urlset']['url']]
        for link in links:
            yield scrapy.Request(link,callback=self.getdatas)
    


    def getdatas(self,response):
        category = response.xpath('.//*[@class="collection__title"]/text()').extract_first()
        links = list(set(response.xpath('.//li/a[@class="product_slider"]/@href').extract()))
        for link in links:
            yield scrapy.Request(response.urljoin(link),callback=self.getdata,meta={
                'cat':category
            })
        

        nextlink = response.xpath('.//link[@rel="next"]/@href').extract_first()
        if nextlink:
            yield scrapy.Request(response.urljoin(nextlink),callback=self.getdatas)
    


    def getdata(self,response):
        link = response.url
        category = response.meta.get('cat')
        jsondata = json.loads(response.xpath('.//*[@type="application/json"][contains(.,"inventory")]/text()').extract_first())

        for data in jsondata:
            name = data['name']
            option_1 = data['option1']
            option_2 = data['option2']
            try:
                price = int(data['price']/100)
            except:
                price = ''
            try:
                original_price = int(data['compare_at_price'])/100
            except:
                original_price = ''
            inventory = data['inventory_quantity']

            with open(f"ethnc_{date}.csv","a",newline="",encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([str(i).strip() if i else i for i in [date,link,category,name,original_price,price,option_1,inventory]])
                print([str(i).strip() if i else i for i in [date,link,category,name,original_price,price,option_1,inventory]])

        

