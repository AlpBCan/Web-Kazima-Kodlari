from typing import Iterable

import scrapy
from scrapy import Request
from ..items import QuoteItem
from scrapy.selector import Selector


class QuotespiderSpider(scrapy.Spider):
    name = "quotespider"

    def start_requests(self):
        yield scrapy.Request('http://quotes.toscrape.com/js/',
                             meta={'playwright': True,
                                   'playwright_include_page': True
                                   })

    async def parse(self, response):
        playwright_page = response.meta['playwright_page']

        while True:
            content = await playwright_page.content()
            selector = Selector(text=content)

            quotes = selector.css('div.quote')

            for quote in quotes:
                quote_item = QuoteItem()
                quote_item['quote'] = quote.css('span.text::text').get()
                quote_item['author'] = quote.css('small.author::text').get()
                tags_string = ''
                tags = quote.css('a.tag::text').getall()
                for tag in tags:
                    tags_string += tag + ' '
                quote_item['tags'] = tags_string.strip()

                yield quote_item

            next_button_link = selector.css('li.next a::attr(href)').get()
            if next_button_link is not None:
                next_button = playwright_page.locator('li.next a')
                await next_button.click()
                await playwright_page.wait_for_timeout(5000)
            else:
                break
