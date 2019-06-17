import scrapy
import csv

class BrickSetSpider(scrapy.Spider):
    name = 'brick_spider'
    start_urls = ['http://brickset.com/sets/year-2016']

    def parse(self, response):
        SET_SELECTOR = '.set'
        for brickset in response.css(SET_SELECTOR):

            NAME_SELECTOR = 'h1 a ::text'
            PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'

            if brickset.xpath(PIECES_SELECTOR).extract_first() == None: 
                peices = 0
            else:
                peices = brickset.xpath(PIECES_SELECTOR).extract_first()

            if  int(peices) > 800:
                expensive = 'yes'
                cheap = 'no'
            else: 
                expensive = 'no'
                cheap = 'yes'

            yield {
                'name': brickset.css(NAME_SELECTOR).extract_first(),
                'pieces': peices,
                'expensive': expensive,
                'cheap': cheap
            }

        NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )