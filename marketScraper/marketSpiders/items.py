# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import datetime
from scrapy import Item, Field
from dataclasses import dataclass

class Product(Item):

    SKU =  Field()
    name=  Field()
    price = Field()
    category1=  Field()
    category2=  Field()
    category3=  Field()
    supermarket=  Field()
    date = Field()

    def set_all(self):
        for keys, _ in self.fields.items():
            self[keys] = None 
