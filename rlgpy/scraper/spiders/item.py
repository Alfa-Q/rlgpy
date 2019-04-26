"""Spider which extracts all Rocket League item data.

Example:
    process = CrawlerProcess({
        'FEED_URI': 'item_data.jl',
        'FEED_FORMAT': 'jsonlines'
    })
    process.crawl(ItemSpider)
    process.start()
    >>> *Scraped Debug Messages*
    Produces a jsonlines file 'item_data.jl' which contains each Rocket League item in JSON format
    separated by newline.

"""

from scrapy.http import Response
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from rlgpy.scraper.items import RlItem


class ItemSpider(CrawlSpider):
    """Spider which crawls and extracts Rocket League item data.

    Attributes:
        name (str): The name of the spider
        allowed_domains (:obj:`list` of :obj:`str`): The domains allowable to crawl.
        start_urls (:obj:`list` of :obj:`str`): The URLs which the spider will begin crawling on.
        rules (:obj:`tuple` of :obj:`scrapy.spiders.Rule`): Additional spider rules for following
            links.
        custom_settings: ItemSpider specific settings, mapping it to the associated pipeline.

    """
    name = 'rl-item'
    allowed_domains = ['rocket-league.com']
    start_urls = ['https://rocket-league.com/items']
    rules = (
        Rule(
            link_extractor=LinkExtractor(allow=(r'/items/*',)),
            callback='parse_item'
        ),
    )
    custom_settings = {
        'ITEM_PIPELINES': {'rlgpy.scraper.pipelines.RlItemPipeline': 300}
    }

    def parse_item(self, response: Response) -> RlItem:
        """Parse items from the item category pages.

        Args:
            response: The response containing the resource from the extracted URL.

        Yields:
            A loaded RlItem.

        """
        self.logger.info('Crawler Found Item Page: %s', response.url)

        # Iterate through each rocket league item and build it.
        for elem_item in response.xpath('//div[starts-with(@class, "item-omg-wtf-bbq")]'):
            loader = ItemLoader(item=RlItem(), selector=elem_item)
            loader.add_xpath('data_id', './/div/@data-id')
            loader.add_xpath('img_url', './/img/@src')
            loader.add_value('name', elem_item.attrib['data-name'])
            loader.add_value('category', elem_item.attrib['data-category'])
            loader.add_value('platform', elem_item.attrib['data-platform'])
            loader.add_value('rarity', elem_item.attrib['data-rarity'])
            loader.add_value('dlcpack', elem_item.attrib['data-dlcpack'])
            yield loader.load_item()
