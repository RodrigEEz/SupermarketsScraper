import scrapy
import utils
from ..items import Product

class vierciSpider(scrapy.Spider):
    name = 'vierci'

    url = ""

    def start_requests(self):

        url = self.url
    
        yield scrapy.Request(
            url=url,
            callback=self.parse
        )

    def parse(self, response):
        
        links = response.xpath('//div[@class = "header-wrapper"]//li[contains(@class,"inactive level1")]//li[@class = "inactive level3"]/a/@href').getall()

        yield from response.follow_all(links, callback=self.parse_page)


    def parse_page(self, response):
        product_links = response.xpath('//div[@class = "item-box"]//a[@class = "picture-link"]/@href').getall()

        yield from response.follow_all(product_links, callback= self.parse_product)

        next_page = response.xpath('//div[@class = "product-pager"]//div[@class = "product-pager-box"]//a[text()[normalize-space(.) = "Siguiente"]]/@href').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


    def parse_product(self, response):

        product = Product()

        product.set_all()
            
        product['name'] = response.xpath('//h1[@class = "productname"]/text()').get().strip()

        product['SKU'] = response.xpath('//div[@class = "sku"]/text()').get().strip().replace('Código de Barras:','')

        product['price'] = int(response.xpath('//span[@class = "productPrice"]/text()').get().strip().replace('.',''))

        categories = utils.clean_list(response.xpath('//div[@class = "breadcrumb"]/text()').getall())

        for i,category in enumerate(('category1', 'category2', 'category3')):
            try:
                product[category] = categories[i]
            except IndexError:
                pass

        product['supermarket'] = 'SUPERSEIS'

        product['date'] = utils.get_today()

        yield product


class stockSpider(vierciSpider):
    name = 'stock'

    url = "https://www.stock.com.py/default.aspx"


class superseisSpider(vierciSpider):
    name = 's6'

    url = "https://www.superseis.com.py/default.aspx"