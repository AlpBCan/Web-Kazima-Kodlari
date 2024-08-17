import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class YelpcrawlerSpider(CrawlSpider):
    name = "yelpcrawler"
    allowed_domains = ["yelp.com"]
    start_urls = ["https://www.yelp.com/search?find_desc=Gyms&find_loc=Berlin%2C+Germany"]

    rules = (Rule(LinkExtractor(allow=r"desc=Gyms.*start=")),
             Rule(LinkExtractor(allow=r"biz/.*osq=Gyms", deny='hrid'), callback="parse_item", follow=False))

    def parse_item(self, response):
        name = response.css('h1.y-css-olzveb::text').get()
        if name is None:
            name = 'Bilgi yok'
        url = response.url

        a_tag = response.xpath('//p[text()="Business website"]/following-sibling::p[1]/a')
        url_on_website = a_tag.css('::text').get()
        if url_on_website is not None:
            if url_on_website[-1] == '…':
                website_link = a_tag.attrib['href']
            else:
                website_link = url_on_website
        else:
            website_link = 'Bilgi yok'

        phone = response.xpath('//p[text()="Phone number"]/following-sibling::p[1]/text()').get()
        if phone is None:
            phone = 'Bilgi yok'

        address = response.xpath('//a[text()="Get Directions"]/../following-sibling::p[1]/text()').get()
        if address is None:
            address = 'Bilgi yok'

        yield {
            'name': name,
            'url': url,
            'website_link': website_link,
            'phone': phone,
            'address': address
        }
