import scrapy
from ..items import TigerItem

class ProductSpider(scrapy.Spider):
    name = "product"
    allowed_domains = ["flyingtiger.com"]
    start_urls = ["https://flyingtiger.com/collections/shop-all"]

    def parse(self, response):
        container = response.css('ul#product-grid')
        items_a_tags = container.css('a.card__information--title')

        for a_tag in items_a_tags:
            product_url = 'https://flyingtiger.com' + a_tag.attrib['href']
            yield scrapy.Request(product_url, callback=self.parse_items)

        next_page_link = response.css('a[aria-label="Next"]')

        if next_page_link:
            yield response.follow(next_page_link.attrib['href'], callback=self.parse)


    def parse_items(self, response):
        tiger_item = TigerItem()

        tiger_item['name'] = response.css('h1.title::text').get().strip()
        tiger_item['price'] = response.css('span.price-item::text').get().strip()
        # Product code: 3054300
        tiger_item['product_code'] = response.css('div.product__sku::text').get().strip().split(':')[-1].strip()
        # //flyingtiger.com/cdn/shop/files/strawberry-serving-bowl-kitchen-flying-tiger-copenhagen-771878.jpg
        try:
            tiger_item['image_url'] = 'https:' + response.css('div.product__media img').attrib['src'].split('?')[0]
        except:
            tiger_item['image_url'] = 'https://t3.ftcdn.net/jpg/04/62/93/66/360_F_462936689_BpEEcxfgMuYPfTaIAOC1tCDurmsno7Sp.jpg'

        tiger_item['product_url'] = response.url

        yield tiger_item

# https://t3.ftcdn.net/jpg/04/62/93/66/360_F_462936689_BpEEcxfgMuYPfTaIAOC1tCDurmsno7Sp.jpg