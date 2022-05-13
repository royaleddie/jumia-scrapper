from ast import IsNot, Not
import scrapy


class JumiaBotSpider(scrapy.Spider):
    name = 'jumia-bot'
    start_urls = ['https://www.jumia.com.ng/catalog/?q=oraimo']

    def parse(self, response):
        for products in response.css('article.c-prd'):
            yield {
                'product_url': products.css('a.core').attrib['href'],
                'image_url': products.css('img.img').attrib['data-src'],
                'product_name': products.css('h3.name::text').get(),
                'product_price': products.css('div.prc::text').get().replace('₦', ''),
                'rating_count': products.css('div.rev::text').get(),  
            }

        next_page = response.css('a.pg').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)