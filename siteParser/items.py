# Define here the models for your scraped items
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ProductItem(Item):
    url = Field()
    name = Field()
    category = Field()
    price = Field()
    count_players = Field()
    time = Field()
    age = Field()
    description = Field()
    year = Field()
    producer = Field()