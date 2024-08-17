# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BookItem(scrapy.Item):
    name = scrapy.Field()
    price_exc_tax = scrapy.Field()
    price_inc_tax = scrapy.Field()
    category = scrapy.Field()
    stars = scrapy.Field()
    upc = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    image_url = scrapy.Field()