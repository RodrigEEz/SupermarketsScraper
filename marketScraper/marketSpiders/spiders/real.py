import scrapy
import marketSpiders.utils as utils
from ..items import Product
import re

class realSpider(scrapy.Spider):         
    name = 'real'

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
           category1 = link.xpath('.//div[@class="menu-top-block"]/text()').get().strip()
           sublinks = link.xpath('.//li[@class ="ui-menu-item level1 parent parent-ul-cat-mega-menu"]')
           alt_sublinks = link.xpath('.//li[@class ="ui-menu-item level1 parent-ul-cat-mega-menu"]')
           sublinks.append(alt_sublinks)
           for sublink in filter(None,sublinks):
                category2 = sublink.xpath('.//a[@class="title-cat-mega-menu"]//span/text()').get()
                sublinks2 = sublink.xpath('.//li[@class = "ui-menu-item level2 "]')
                if sublinks2 == []:
                    category3 = category2
                    products_link = sublink.xpath('.//a/@href').get()
                    yield response.follow(
                        products_link,
                        callback=self.parse_page, 
                        cb_kwargs={"1": category1,"2": category2,"3" : category3}
                        )
                else:
                    for sublink2 in sublinks2:
                        products_link = sublink2.xpath('.//a/@href').get()
                        category3 = sublink2.xpath('.//span/text()').get().strip()
                        yield response.follow(
                            products_link,
                            callback=self.parse_page, 
                            cb_kwargs={"1": category1,"2": category2,"3" : category3}
                            )

    def parse_page(self, response, **kwargs):
        product_links = response.xpath('//a[@class = "product-item-link"]/@href').getall()

        yield from response.follow_all(product_links, callback= self.parse_product, cb_kwargs=kwargs)

        next_page = response.xpath('//li[@class="item pages-item-next"]//@href').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_page, cb_kwargs=kwargs)

    def parse_product(self, response, **kwargs):

        product = Product()
        product.set_all()

        name = response.xpath('//span[@class="base"]/text()').get().strip()
        product['name'] = name.upper()

        sku = response.xpath('//div[@itemprop="sku"]/text()').get().strip()
        product['SKU'] = sku.upper()

        price = response.xpath('//span[@class="price"]/text()').get().strip()
        product['price'] = int(re.sub('[^0-9]','', price))

        for i,category in enumerate(('category1', 'category2', 'category3')):
            try:
                product[category] = kwargs[str(i+1)].upper()
            except IndexError:
                pass

        product['supermarket'] = 'REAL'

        product['date'] = utils.get_today()

        yield product