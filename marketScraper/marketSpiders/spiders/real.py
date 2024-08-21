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
            callback=self.follow_categories
        )


    def follow_categories(self, response):
       """Follows every product category link"""
       
       links = response.xpath('//div[@class="level0 submenu"]//li[@class = "ui-menu-item level2 "]//a/@href').getall()
       alt_links = response.xpath('.//li[@class ="ui-menu-item level1 parent-ul-cat-mega-menu"]//a/@href').getall()
       links.append(alt_links)
       links = filter(None,links)

       yield from response.follow_all(links,callback=self.follow_products) 


    def follow_products(self, response):
        """Follows every product link"""

        # extract category levels from URL so it can be passed to the product parsing
        categories = re.sub('(-0)|(\\.html)|(^(.*?)\\.py/)', '', response.request.url)
        categories = [x.replace('-',' ') for x in categories.split('/')]
        keys = ['1', '2', '3']
        if len(categories) < 3: categories[2] = categories[1]
        categories = dict(zip(keys,categories)) 

        # product links
        product_links = response.xpath('//a[@class = "product-item-link"]/@href').getall()

        yield from response.follow_all(product_links, callback= self.parse_product, cb_kwargs=categories)

        # next page link
        next_page = response.xpath('//li[@class="item pages-item-next"]//@href').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.follow_products)

    def parse_product(self, response, **kwargs):
        """Parses product information. Every string is uppercased"""

        product = Product()
        product.set_all()

        name = response.xpath('//span[@class="base"]/text()').get().strip()
        product['name'] = name.upper()

        sku = response.xpath('//div[@itemprop="sku"]/text()').get().strip()
        product['SKU'] = sku.upper()

        price = response.xpath('//span[@class="price"]/text()').get().strip()
        product['price'] = int(re.sub('[^0-9]','', price))

        for i,category in enumerate(('category1', 'category2', 'category3')):
                product[category] = kwargs[str(i+1)].upper()

        product['supermarket'] = 'REAL'

        product['date'] = utils.get_today()

        yield product