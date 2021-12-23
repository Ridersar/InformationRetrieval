# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class SiteparserPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.connection = sqlite3.connect("shop.db")
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS products""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS products(
                                                url TEXT,
                                                name TEXT,
                                                category TEXT,
                                                price TEXT,
                                                count_players TEXT,
                                                time TEXT,
                                                age TEXT,
                                                description TEXT,
                                                year TEXT,
                                                producer TEXT
                                                )""")

    def process_item(self, item, spider):
        self.put_in_table(item)
        return item

    def put_in_table(self, item):
        self.cursor.execute("""INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
                                    item['url'],
                                    item['name'],
                                    item['category'],
                                    item['price'],
                                    item['count_players'],
                                    item['time'],
                                    item['age'],
                                    item['description'],
                                    item['year'],
                                    item['producer']
                                )
                            )
        self.connection.commit()
