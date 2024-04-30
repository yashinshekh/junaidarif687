import scrapy
import json
import xmltodict
import csv
import datetime
import os
import re

date = datetime.datetime.today().strftime('%m_%d_%y')

class SapphireonlineSpider(scrapy.Spider):
    name = "sapphireonline"
    start_urls = ["https://pk.sapphireonline.pk/sitemap_collections_1.xml"]

    custom_settings = {
        "DOWNLOAD_DELAY":1
    }

    if f"sapphireonline_{date}.csv" not in os.listdir(os.getcwd()):
        with open(f"sapphireonline_{date}.csv","a") as f:
            writer = csv.writer(f)
            writer.writerow(['date','link','category','title','old_price','new_price','option','quantity'])


    def parse(self, response,*args):
        links = [i['loc'] for i in json.loads(json.dumps(xmltodict.parse(response.text)))['urlset']['url']]
        for link in links:
            link = link+'?page=1'
            yield scrapy.Request(
                link,
                callback=self.getdatas,
                meta={
                    'link':link,
                    'page':2
                }
            )

            # break


    def getdatas(self,response):
        links = response.xpath('.//*[@class="t4s-product-title"]/a/@href').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link),callback=self.getdata)

        if links:
            yield scrapy.Request(
                response.meta.get('link').replace('?page=1',f'?page={response.meta.get("page")}'),
                callback=self.getdatas,
                meta={
                    'link':response.meta.get('link'),
                    'page':response.meta.get('page')+1
                })

    def getdata(self,response):
        category = response.xpath('.//*[@class="t4s-pr-breadcrumb"]/a[2]/text()').extract_first()
        title = response.xpath('.//*[@class="t4s-pr-breadcrumb"]/span/text()').extract_first()
        old_price = response.xpath('.//del/span/text()').extract_first()
        new_price = response.xpath('.//ins/span/text() | .//*[@class="t4s-product-price"]/span/text()').extract_first()

        datas = response.xpath('.//select/option').extract()
        for data in datas:
            sel = scrapy.Selector(text=data)

            option = sel.xpath('.//option/text()').extract_first()
            quantity = sel.xpath('.//option/@data-inventoryquantity').extract_first()

            if quantity == "0":
                quantity = "Out of stock"

            with open(f"sapphireonline_{date}.csv","a") as f:
                writer = csv.writer(f)
                writer.writerow([date,response.url,category,title,old_price,new_price,option,quantity])
                print([date,response.url,category,title,old_price,new_price,option,quantity])


        if not datas:
            option = ''
            quantity = ''.join(re.findall(r'\d+',response.xpath('.//span/text()[contains(.,"-Piece")]').extract_first()))
            with open(f"sapphireonline_{date}.csv","a") as f:
                writer = csv.writer(f)
                writer.writerow([date,response.url,category,title,old_price,new_price,option,quantity])

