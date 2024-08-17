import scrapy
from ..items import QuoteItem


class QuotespiderSpider(scrapy.Spider):
    name = "quotespider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        quote_list = response.css('div.quote')
        for one_quote in quote_list:
            quote_item = QuoteItem()

            quote = one_quote.css('span.text::text').get()

            author = one_quote.css('small.author::text').get()

            tag_list = []

            tag_elements = one_quote.css('a.tag')
            for tag in tag_elements:
                tag_list.append(tag.css('::text').get())

            tags = ', '.join(tag_list).strip()

            quote_item['quote'] = quote
            quote_item['author'] = author
            quote_item['tags'] = tags

            yield quote_item

        next_page_link = response.css('li.next a::attr(href)').get()

        if next_page_link is not None:
            yield response.follow(next_page_link, callback=self.parse)

