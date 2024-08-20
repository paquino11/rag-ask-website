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


def scrape(start_url, output_file='output.json', obey_robots_txt=True,
               concurrent_requests=8, download_delay=1, depth_limit=5):
    """
    Run the WebsiteSpider with the given parameters.

    :param start_url: The starting URL for the spider.
    :param output_file: The name of the output file where the scraped data will be saved.
    :param obey_robots_txt: Whether to obey robots.txt rules.
    :param concurrent_requests: The number of concurrent requests Scrapy will make.
    :param download_delay: The delay (in seconds) between requests.
    :param depth_limit: The depth limit for following links.
    """
    
    # Disable logging to console
    logging.getLogger('scrapy').setLevel(logging.CRITICAL)

    process = CrawlerProcess(settings={
        'FEEDS': {
            output_file: {
                'format': 'json',
                'overwrite': True
            },
        },
        'LOG_LEVEL': 'CRITICAL',  # Set to 'ERROR' or 'CRITICAL' to minimize logs
        'ROBOTSTXT_OBEY': obey_robots_txt,
        'CONCURRENT_REQUESTS': concurrent_requests,
        'DOWNLOAD_DELAY': download_delay,
        'DEPTH_LIMIT': depth_limit,
    })

    process.crawl(WebsiteSpider, start_url=start_url)
    process.start()

# Example usage
# if __name__ == "__main__":
#     scrape(start_url='https://docs.crewai.com')
