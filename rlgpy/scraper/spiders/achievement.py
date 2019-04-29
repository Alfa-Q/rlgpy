"""Spider which extracts all Rocket League achievement data.

Example:
    >>> from rlgpy.scraper.spiders import AchievementSpider
    >>> from scrapy.crawler import CrawlerProcess
    >>> process = CrawlerProcess({
    >>>    'FEED_URI': 'achievement_data.jl',
    >>>    'FEED_FORMAT': 'jsonlines'
    >>> })
    >>> process.crawl(AchievementSpider)
    >>> process.start()
    Produces a jsonlines file 'achievement_data.jl' which contains each Rocket League achievement
    in JSON format separated by newline.

"""

import scrapy
from scrapy.http import Response

from rlgpy.scraper.items import (
    RlAchievementLoader,
    RlAchievement
)


class AchievementSpider(scrapy.Spider):
    """Spider which extracts Rocket League achievement data.

    Attributes:
        name (str): The name of the spider
        allowed_domains (List[str]): The domains allowable to crawl.
        start_urls (List[str]): The URLs which the spider will begin scraping at.

    """

    name = 'rl-achievement'
    allowed_domains = ['rocket-league.com']
    start_urls = ['https://rocket-league.com/trophies']
    custom_settings = {
        'ITEM_PIPELINES': {'rlgpy.scraper.pipelines.RlAchievementPipeline': 300}
    }


    def parse(self, response: Response) -> RlAchievement:
        """Parse achievements on the achievement page.

        Args:
            response: The response containing the resource from the extracted URL.

        Yields:
            A loaded achievement item.

        """
        self.logger.info('Crawler Found Achievement Page: %s', response.url)

        for achievement in response.css('div.rlg-trophies-trophy'):
            loader = RlAchievementLoader(item=RlAchievement(), selector=achievement)
            loader.add_css('name', 'img::attr(alt)')
            loader.add_css('img_url', 'img::attr(src)')
            loader.add_css('gamerscore', 'li.rlg-trophies-trophy-info-gamerscore span::text')
            loader.add_css('trophy_type', 'li.rlg-trophies-trophy-info-trophy', re=r'(?<=\_)(.*?)(?=\_)')
            loader.add_css('description', 'p::text')
            yield loader.load_item()
