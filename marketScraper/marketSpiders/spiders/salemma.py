import scrapy
import marketSpiders.utils as utils
from ..items import Product
import re


class SalemmaSpider(scrapy.Spider):
    name = 'salemma'

    url = "https://www.salemmaonline.com.py/"

    def start_requests(self):

        url = self.url
    
        yield scrapy.Request(
            url=url,
            callback=self.follow_categories
        )


    def follow_categories(self, response):
      """Follows every product category link"""
        
      links = response.xpath('//div[@class = "panel panel-default"][position()>=3]//a[@class = "c-title "]/@href').getall()

      yield from response.follow_all(links, callback=self.follow_products)


    def follow_products(self, response):
      """Follows every product link"""

      # extract category levels from URL so it can be passed to the product parsing
      categories = re.sub('(^(.*?)\\.py/)|(\\?.+)', '', response.request.url)
      categories = [x.replace('-',' ') for x in categories.split('/')]
      keys = ['1', '2', '3']
      if len(categories) < 3: categories[2] = categories[1]
      categories = dict(zip(keys,categories)) 

      # product links
      product_links = response.xpath('//a[@class="apsubtitle"]/@href').getall()

      yield from response.follow_all(product_links, callback=self.parse_product, cb_kwargs=categories)

      #next page link
      next_page = response.xpath('//a[@rel="next"]/@href').get()

      if next_page is not None:
         yield response.follow(next_page, callback=self.follow_products)


    def parse_product(self, response, **kwargs):
        """Parses product information. Every string is uppercased"""

        print(kwargs)

        product = Product()

        product.set_all()
            
        name = response.xpath('//p[@class="titledetails"]//text()').get().strip() + \
                        " " + response.xpath('//p[@class="pdivtitledetails"]//text()').get().strip()
        product['name'] = name.upper()

        product['SKU'] = response.xpath('//p[@class="pricedetails-off"]//text()').get().replace('Codigo:','').strip()

        price = response.xpath('//p[@class="pricedetails-off"]//text()').getall()[1].strip()
        product['price'] = int(re.sub('[^0-9]','',price))

        for i,category in enumerate(('category1', 'category2', 'category3')):
                product[category] = kwargs[str(i+1)].upper()

        product['supermarket'] = 'SALEMMA'

        product['date'] = utils.get_today()

        yield product