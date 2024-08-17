# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import openpyxl
import sqlite3


class BooksPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter['name'] = adapter['name'].upper()
        # 19
        available_no = adapter.get('availability').split('(')[-1].split()[0]
        adapter['availability'] = available_no
        adapter['price_exc_tax'] = adapter.get('price_exc_tax').replace('£', '$')
        adapter['price_inc_tax'] = adapter.get('price_inc_tax').replace('£', '$')
        adapter['tax'] = adapter.get('tax').replace('£', '$')

        return item


class DropperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        available_no = adapter.get('availability').split('(')[-1].split()[0]
        if int(available_no) >= 10:
            adapter['availability'] = available_no
            adapter['price_exc_tax'] = adapter.get('price_exc_tax').replace('£', '$')
            adapter['price_inc_tax'] = adapter.get('price_inc_tax').replace('£', '$')
            adapter['tax'] = adapter.get('tax').replace('£', '$')
            adapter['name'] = adapter['name'].upper()

            return item
        else:
            raise DropItem(f'{adapter['name']} için yeterli stok yok')


class ExcelPipeline:
    def open_spider(self, spider):
        self.workbook = openpyxl.Workbook()
        self.sheet = self.workbook.active
        self.sheet.title = 'Books'
        self.sheet.append(['name',
                          'price_exc_tax',
                          'price_inc_tax',
                          'category',
                          'stars',
                          'upc',
                          'tax',
                          'availability',
                          'image_url'])

    def process_item(self, item, spider):
        self.sheet.append([item.get('name'),
                           item.get('price_exc_tax'),
                           item.get('price_inc_tax'),
                           item.get('category'),
                           item.get('stars'),
                           item.get('upc'),
                           item.get('tax'),
                           item.get('availability'),
                           item.get('image_url'),
                           ])
        return item

    def close_spider(self, spider):
        self.workbook.save('excelpipelines_.xlsx')


class SQLitePipeline:

    def open_spider(self, spider):
        self.connection = sqlite3.connect("bookdatabase.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS booktable (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price_exc_tax TEXT,
                price_inc_tax TEXT,
                category TEXT,
                stars TEXT,
                upc TEXT,
                tax TEXT,
                availability TEXT,
                image_url TEXT
            )
        ''')
        self.connection.commit()

    def process_item(self, item, spider):
        self.cursor.execute('''
            INSERT INTO booktable (
                name, price_exc_tax, price_inc_tax, category, stars, upc, tax, availability, image_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item['name'],
            item['price_exc_tax'],
            item['price_inc_tax'],
            item['category'],
            item['stars'],
            item['upc'],
            item['tax'],
            item['availability'],
            item['image_url']
        ))
        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.connection.close()