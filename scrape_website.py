import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse, urljoin
import logging


class WebsiteSpider(scrapy.Spider):
    name = 'website'

    def __init__(self, start_url=None, *args, **kwargs):
        super(WebsiteSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.allowed_domains = [urlparse(start_url).netloc]

    def parse(self, response):
        yield {
            'url': response.url,
            'title': response.css('title::text').get(),
            'content': ' '.join(response.css('p::text').getall()),
        }

        for href in response.css('a::attr(href)'):
            url = urljoin(response.url, href.get())
            if url.startswith('http'):
                yield response.follow(url, self.parse)


def scrape(start_url, output_file='output.json'):
    """
    Run the WebsiteSpider with the given parameters.

    :param start_url: The starting URL for the spider.
    """
    
    logging.getLogger('scrapy').setLevel(logging.CRITICAL)

    process = CrawlerProcess(settings={
        'FEEDS': {
            output_file: {
                'format': 'json',
                'overwrite': True
            },
        },
        'LOG_LEVEL': 'CRITICAL',
        'ROBOTSTXT_OBEY': True,
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 1,
        'DEPTH_LIMIT': 5,
    })

    process.crawl(WebsiteSpider, start_url=start_url)
    process.start()

# Example usage
# if __name__ == "__main__":
#     scrape(start_url='https://docs.crewai.com')
