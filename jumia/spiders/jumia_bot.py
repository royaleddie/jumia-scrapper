from ast import IsNot, Not
import scrapy


class JumiaBotSpider(scrapy.Spider):
    name = 'jumia-bot'
    start_urls = ['https://www.jumia.com.ng/catalog/?q=oraimo']

    def parse(self, response):
        for products in response.css('a.core'):
            if(products.css('h3.name::text').get() and products.css('div.prc::text').get()):
                yield {
                    'product_url': 'https://jumia.com.ng'+products.attrib['href'],
                    'image_url': products.css('img.img').attrib['data-src'],
                    'product_name': products.css('h3.name::text').get(),
                    'product_price': products.css('div.prc::text').get().replace('₦', '').strip() if '₦' in products.css('div.prc::text').get() else products.css('div.prc::text').get(),
                    'product_rating': products.css('div.rev::text').get()
                }
        next_page = response.xpath('//*[@id="jm"]/main/div[2]/div[3]/section/div[2]/a[6]') 
        if next_page and next_page.attrib['href']: 
            next_page_url = 'https://jumia.com.ng'+next_page.attrib['href'] 
            yield response.follow(next_page_url, callback = self.parse)
        