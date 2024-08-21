import scrapy
import marketSpiders.utils as utils
from ..items import Product
import re

class vierciSpider(scrapy.Spider):
    """Spider for vierci supermarkets. Both supermarkets owned by Grupo Vierci use the same webpage structure"""

    name = 'vierci'

    url = ""

    def start_requests(self):

        url = self.url
    
        yield scrapy.Request(
            url=url,
            callback=self.follow_categories
        )


    def follow_categories(self, response):
        """Follows every product category link"""
        
        links = response.xpath('//div[@class = "header-wrapper"]//li[@class = "inactive level3"]/a/@href').getall()

        yield from response.follow_all(links, callback=self.follow_products)


    def follow_products(self, response):
        """Follows every product link"""

        # product links
        product_links = response.xpath('//div[@class = "item-box"]//a[@class = "picture-link"]/@href').getall()
        yield from response.follow_all(product_links, callback= self.parse_product)

        # next page link
        next_page = response.xpath('//a[text()[normalize-space(.) = "Siguiente"]]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.follow_products)


    def parse_product(self, response):
        """Parses product information. Every string is uppercased"""

        product = Product()

        product.set_all()
            
        name = response.xpath('//h1[@class = "productname"]/text()').get().strip()
        product['name'] = name.upper()

        sku = response.xpath('//div[@class = "sku"]/text()').get().strip().replace('Código de Barras:','')
        product['SKU'] = sku.upper()

        price = response.xpath('//span[@class = "productPrice"]/text()').get().strip()
        product['price'] = int(re.sub('[^0-9]','', price))

        categories = utils.clean_list(response.xpath('//div[@class = "breadcrumb"]/text()').getall())

        for i,category in enumerate(('category1', 'category2', 'category3')):
            try:
                product[category] = categories[i].upper()
            except IndexError:
                # if no level 3 category exists, copies level 2 category
                product[category] = categories[i-1].upper()

        product['supermarket'] = 'SUPERSEIS'

        product['date'] = utils.get_today()

        yield product


class stockSpider(vierciSpider):
    name = 'stock'

    url = "https://www.stock.com.py/default.aspx"


class superseisSpider(vierciSpider):
    name = 's6'

    url = "https://www.superseis.com.py/default.aspx"