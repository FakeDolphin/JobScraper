import scrapy
from JobScraper.Bulldog_scraper.Scraper.items import *


class BulldogScraper(scrapy.Spider):
    name = "bulldogscraper"

    start_urls = [
        # 'https://www.indeed.com/jobs?q=python+developer&start=0&vjk=740129074730054a',
        'https://bulldogjob.pl/companies/jobs/s/page,1',
    ]
    custom_settings = {
        # 'COOKIES_ENABLED': False,
        # 'DEFAULT_REQUEST_HEADERS': {
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
        #     "Accept-Encoding": "gzip, deflate", 
        #     "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8", 
        #     "Dnt": "1", 
        #     "Host": "httpbin.org", 
        #     "Upgrade-Insecure-Requests": "1", 
        #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        # },
        # 'SPIDER_MIDDLEWARES': {
        #     'JobScraper.Bulldog_scraper.Scraper.middlewares.ScraperSpiderMiddleware': 543,
        # },
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'JobScraper.Bulldog_scraper.Scraper.middlewares.ScraperDownloaderMiddleware': 543,
        # },
        'ITEM_PIPELINES': {
            'JobScraper.Bulldog_scraper.Scraper.pipelines.ScraperPipeline': 300,
        },
        'MONGO_URI': 'mongodb://127.0.0.1/?authSource=jobscrapper',
        'MONGO_DATABASE': 'jobscrapper',
    }
    
    # def start_requests(self):
    #     print(f"Existing settings: {self.settings.attributes.keys()}")
    #     urls = [
    #         'https://www.indeed.com/jobs?q=python+developer&start=0&vjk=740129074730054a',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        blocks = response.xpath('//div[@class="py-6 md:py-8 px-8 flex flex-wrap relative bg-white mb-2 rounded-lg shadow "]')
        if blocks:
            for block in blocks:
                title = block.xpath('.//h3[@class="text-c28 font-medium mb-3 hidden md:block"]/a/text()').extract_first()
                description = ''
                company = ''
                place = block.xpath('.//div[@class="relative rounded-t-lg px-2 -ml-2 z-10 "]/text()').extract_first()
                link = block.xpath('.//a[@class="absolute top-0 left-0 w-full h-full"]/@href').extract_first()
                salary = block.xpath('.//p[@class="text-purple"]/text()').extract_first() or '-'
                
                stack_list = block.xpath('.//span[@class="pr-3 font-medium overflow-hidden overflow-ellipsis"]')
                stack = [record.xpath('.//text()').get() for record in stack_list]

                work_type = ''
                work_time = ''
                yield ScraperItem(title=title, link=link, salary=salary, place=place, stack=stack)
                # need to avoid captcha, take proxy and opening a page
                
            next_page = int(response.url.split('page,')[1]) + 1
            next_page_url = response.url.split(',')[0] + ',' + str(next_page)
            if next_page_url is not None:
                yield scrapy.Request(response.urljoin(next_page_url))
                