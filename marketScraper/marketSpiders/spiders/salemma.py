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
            callback=self.parse
        )

    def parse(self, response):
        
      links = response.xpath('//div[@class = "panel panel-default"]')

      for link in links[2:]:
         sublinks = link.xpath('.//a[@class = "c-title "]/@href').getall()
         yield from response.follow_all(sublinks, callback=self.parse_page)



        
      """links = response.xpath('//div[@class = "header-wrapper"]//li[contains(@class,"inactive level1")]//li[@class = "inactive level3"]/a/@href').getall()

        yield from response.follow_all(links, callback=self.parse_page)"""


    def parse_page(self, response):

      product_links = response.xpath('//a[@class="apsubtitle"]/@href').getall()
      
      categories = re.sub('\\?.+','',re.sub('^(.*?)\\.py/', '', response.request.url))
      categories = [x.replace('-',' ') for x in categories.split('/')]
      if len(categories) == 2: categories.append(categories[1]) 
      keys = ['1', '2', '3']
      categories = dict(zip(keys,categories))
      

      yield from response.follow_all(product_links, callback=self.parse_product, cb_kwargs=categories)

      next_page = response.xpath('//a[@rel="next"]/@href').get()

      if next_page is not None:
         yield response.follow(next_page, callback=self.parse_page)


    def parse_product(self, response, **kwargs):

        print(kwargs)

        product = Product()

        product.set_all()
            
        name = response.xpath('//p[@class="titledetails"]//text()').get().strip() + \
                        " " + response.xpath('//p[@class="pdivtitledetails"]//text()').get().strip()
        product['name'] = name.upper()

        product['SKU'] = response.xpath('//p[@class="pricedetails-off"]//text()').get().strip().replace('Codigo:','')

        price = response.xpath('//p[@class="pricedetails-off"]//text()').getall()[1].strip()
        product['price'] = int(re.sub('[^0-9]','',price))

        for i,category in enumerate(('category1', 'category2', 'category3')):
            try:
                product[category] = kwargs[str(i+1)].upper()
            except IndexError:
                pass

        product['supermarket'] = 'SALEMMA'

        product['date'] = utils.get_today()

        yield product