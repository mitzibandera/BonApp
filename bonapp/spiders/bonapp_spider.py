from scrapy import Spider, Request
from bonapp.items import BonappItem
import re

class BonappSpider(Spider):

    name = "bonapp_spider"
    allowed_domains = ['www.bonappetit.com']
    start_urls = ['https://www.bonappetit.com/ingredient/pasta']


    def parse(self, response):

        blog_titles = response.xpath('//div[@class="feature-item-content"]')
        blog_links = [f'https://www.bonappetit.com{lnk}' for lnk in blog_titles.xpath('.//a/@href').extract()]
        for url in blog_links[:1]:
            yield Request(url = url, callback = self.parse_gallery_page)
      

    def parse_gallery_page(self, response):

        if bool(response.xpath('//div[@class="ingredients__text"]/text()').extract()):
            yield Request(url = self, callback = self.parse_recipe_page)

        elif bool(response.xpath('//div[@class="content-card-embed__info"]//a/@href').extract()):
            recipe_link = [f'https://www.bonappetit.com{lnk}' for lnk in response.xpath('//div[@class="content-card-embed__info"]//a/@href').extract()]
            yield Request(url = recipe_link, callback = self.parse_recipe_page)

        else:
            recipes_link = response.xpath('//div[@class="gallery-slid-caption__cta-block"]//a/@href').extract()
            for url in recipes_link:
                yield Request(url = url, callback = self.parse_recipe_page)


    def parse_recipe_page(self, response):

        Name = response.xpath('//a[@name="top"]/text()').extract()
        Ingredients = response.xpath('//div[@class="ingredients__text"]/text()').extract()
        # if response.xpath('./div/a'):
        #     Ingredients.append(response.xpath('./div/a/text()').extract()[0] + Ingredient)

        item = BonappItem()
        item["Ingredients"] = Ingredients
        item["DishTitle"] = Name

        yield item





