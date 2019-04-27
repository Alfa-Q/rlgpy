"""Spider which extracts all Rocket League trade data.

Examples:
    >>> from scrapy.crawler import CrawlerProcess
    >>> process = CrawlerProcess({
    >>>    'FEED_URI': 'trade_data.jl',
    >>>    'FEED_FORMAT': 'jsonlines'
    >>> })
    >>> process.crawl(TradeSpider)
    >>> process.start()
    Produces a jsonlines file 'trade_data.jl' which contains each Rocket League item in JSON format
    separated by newline.

    You can also use this spider to crawl other trade-pages with parameters in the URL.
    For example, if you would like to instead scrape the most recent trades for a Rocket League
    item with data_id '773' you just need to overwrite the start_url list and execute the process
    as shown in the previous example.
    >>> TradeSpider.start_urls=[
    >>>     'https://rocket-league.com/trading?filterItem=733&filterCertification=0&...'
    >>> ]

"""

from typing import List

from scrapy.selector import Selector
from scrapy.http import Response
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from rlgpy.scraper.items import (
    RlTradeLoader,
    RlTrade,
    RlTradeableItemLoader,
    RlTradeableItem
)


class TradeSpider(CrawlSpider):
    """Spider which crawls and extracts Rocket League trade data.

    Attributes:
        name (str): The name of the spider
        allowed_domains (:obj:`list` of :obj:`str`): The domains allowable to crawl.
        start_urls (:obj:`list` of :obj:`str`): The URLs which the spider will begin crawling on.
        rules (:obj:`tuple` of :obj:`scrapy.spiders.Rule`): Additional spider rules for following
            links.
        custom_settings: ItemSpider specific settings, mapping it to the associated pipeline.

    """
    name = 'rl-trade'
    allowed_domains = ['rocket-league.com']
    start_urls = ['https://rocket-league.com/trading?p=1']
    rules = (
        Rule(
            link_extractor=LinkExtractor(allow=(r'/trading\?p=\d*',)),
            callback='parse_trades'
        ),
    )
    custom_settings = {
        'CONCURRENT_REQUESTS': 5,
        'CLOSESPIDER_ITEMCOUNT': 10000,
        'CLOSESPIDER_PAGECOUNT': 2,
        'ITEM_PIPELINES': {'rlgpy.scraper.pipelines.RlTradePipeline': 300}
    }

    def parse_items(self, selector: Selector) -> List[RlTradeableItem]:
        """Parse the trade items from the provided selector.

        Extracts each trade item from the provided selector and and loads them into a list to be
        added to the trade object.

        Args:
            selector: The element selector which contains direct children elements that represent
                the trade items.

        Returns: A list of tradeable items.

        """

        items = list()
        for item in selector:
            loader = RlTradeableItemLoader(item=RlTradeableItem(), selector=item)
            loader.add_css('data_id', 'a::attr(href)', re=r'(?<=filterItem=)(\d*)')
            loader.add_css('count', 'div.rlg-trade-display-item__amount::text', re=r'\d+')
            loader.add_css('certification', 'div div div span::text')
            loader.add_css('paint', '[class="rlg-trade-display-item-paint"]::attr(data-name)')
            items.append(loader.load_item())
        return items


    def parse_trades(self, response: Response) -> RlTrade:
        """Parse trades on the current page.

        Args:
            response: The response containing the resource from the extracted URL.

        Yields:
            A loaded trade item.

        """

        self.logger.info('Crawler Found Trade Page: %s', response.url)

        for trade in response.css('div.is--user'):
            loader = RlTradeLoader(item=RlTrade(), selector=trade)
            loader.add_css('data_id', '[name="bookmark"]::attr(data-alias)')
            loader.add_css('url', 'div:first-child a::attr(href)')
            loader.add_css('platform', 'div.rlg-trade-platform-name span::text', re=r'([^\s:]+)')
            loader.add_css('rlg_username', 'div.rlg-trade__avatar img::attr(alt)')
            loader.add_value('have', self.parse_items(trade.css('div#rlg-youritems a')))
            loader.add_value('want', self.parse_items(trade.css('div#rlg-theiritems a')))
            yield loader.load_item()
