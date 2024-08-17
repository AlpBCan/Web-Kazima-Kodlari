# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from .items import TigerItem, ImageItem
from scrapy.pipelines.images import ImagesPipeline



class TigerPipeline:
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open('flying_tiger_data_.json', 'w', encoding='utf-8')
        self.file.write('[\n')

    def process_item(self, item, spider):
        if isinstance(item, TigerItem):
            line = json.dumps(dict(item), ensure_ascii=False) + ',\n'
            self.file.write(line)
            return item
        else:
            return item

    def close_spipder(self, spider):
        self.file.write(']')
        self.file.close()

class CustomImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if isinstance(item, ImageItem):
            yield scrapy.Request(item['image_url'], meta={'item': item})

    def file_path(self, request, response=None, info=None, *, item=None):
        image_name = request.meta['item']['product_code']
        return f'{image_name}.jpg'