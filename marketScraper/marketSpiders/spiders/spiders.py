import scrapy
import utils
from ..items import Product
from .vierci import *

class realSpider(scrapy.Spider):
    name = 'real'

    url = ''

    def start_requests(self):

        url = self.url

        yield scrapy.Request(
            url=url,
            callback=self.parse
        )

    def parse(self, response):

        links = response.xpath()

class testSpider(scrapy.Spider):         
    name = 'test'

    url = "https://www.realonline.com.py/"

    def start_requests(self):

        url = self.url
    
        yield scrapy.Request(
            url=url,
            callback=self.parse
        )

    def parse(self, response):
       
       links = response.xpath('//div[@class="level0 submenu"]')

       for link in links:
           print(link.xpath('.//div[@class="menu-top-block"]/text()').get().strip())

       #yield from response.follow_all(links, callback=self.parse_page)


    def parse_page(self, response):
        # product_links = response.xpath('//div[@class = "item-box"]//a[@class = "picture-link"]/@href').getall()

        # yield from response.follow_all(product_links, callback= self.parse_product)

        # next_page = response.xpath('//div[@class = "product-pager"]//div[@class = "product-pager-box"]//a[text()[normalize-space(.) = "Siguiente"]]/@href').get()

        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)
        print(response)


    #def parse_product(self, response):

