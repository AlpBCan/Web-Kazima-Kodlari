# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TigerItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    product_code = scrapy.Field()
    image_url = scrapy.Field()
    product_url = scrapy.Field()


class ImageItem(scrapy.Item):
    image_url = scrapy.Field()
    product_code = scrapy.Field()