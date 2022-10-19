# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    description = scrapy.Field()
    company = scrapy.Field()
    place = scrapy.Field() # City, Country
    link = scrapy.Field()
    salary = scrapy.Field()
    stack = scrapy.Field()
    work_time = scrapy.Field() # Full-time/Part-time
    work_type = scrapy.Field() # Office/remote
