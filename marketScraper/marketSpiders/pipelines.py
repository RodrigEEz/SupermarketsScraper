# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import marketSpiders.utils as utils


class DatabaseInsert:
    
    def __init__(self):
        self.con = utils.define_connection()

        self.cur = self.con.cursor()

    def process_item(self, item, spider):

        self.cur.execute("""
            INSERT INTO PRODUCTS (SKU, name, price, category1, category2, category3, supermarket, date)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
            """,
            (
                item['SKU'],
                item['name'],
                item['price'],
                item['category1'],
                item['category2'],
                item['category3'],
                item['supermarket'],
                item['date']
            )
        )

        self.con.commit()
        return item
