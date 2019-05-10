"""RLG package API."""

import uuid
from typing import Dict, Any, List

from scrapy.spiders import Spider

from rlgpy.scraper.runners import SafeSpiderRunner
from rlgpy.scraper.spiders import (
    ItemSpider,
    TradeSpider,
    AchievementSpider
)


class RocketLeagueGarage:
    """Rocket League Garage API functions."""

    @staticmethod
    def _run_spider(spider: Spider, settings: Dict[str, Any],
                    delete_file: bool = True) -> List[Dict[str, Any]]:
        """Run the spider until done and return the data.

        Args:
            spider: The scrapy spider to run.
            settings: The settings to run the spider with.
            delete_file: Delete the data file created by the spider.

        Returns:
            A list of the data in JSON format.

        """
        return SafeSpiderRunner.run(
            spider=spider,
            settings=settings,
            delete_file=delete_file
        )


    @classmethod
    def get_items(cls, cache_enabled: bool = True) -> List[Dict[str, Any]]:
        """Retrieve item data from RLG or cache.

        If a request has already been made to the server and the `cache_enabled` is set to `True`,
        subsequent function calls will use a cached version of the webpage.

        It is recommended to use the default value to reduce overloading the server with requests
        and to improve program speed. The only time this would ever need to be changed is in the
        case that new items are added to the site (during a new update).

        Args:
            cache_enabled: Get item data from cached webpage.

        Returns:
            A list of items in JSON format.

        """
        items = RocketLeagueGarage._run_spider(
            spider=ItemSpider,
            settings={
                'FEED_URI': 'item_data_%s.jl' % str(uuid.uuid4()),
                'HTTPCACHE_ENABLED': cache_enabled,
                'HTTPCACHE_EXPIRATION_SECS': 0
            }
        )
        return items


    @classmethod
    def get_trades(cls, url: str = None, max_trades: int = 100,
                   concurrent_c: int = 5) -> List[Dict[str, Any]]:
        """Retrieve trade data from RLG.

        Args:
            url: A custom starting URL. Defaults to first trade page.
            max_trades: Maximum number of trades that will be retrieved from RLG.
            concurrent_c: The total number of concurrent requests that can be made to the server.

        Returns:
            A list of trades in JSON format.

        """
        TradeSpider.start_urls = [url] if url else TradeSpider.start_urls
        trades = RocketLeagueGarage._run_spider(
            spider=TradeSpider,
            settings={
                'CONCURRENT_REQUESTS': concurrent_c,
                'FEED_URI': 'trade_data_%s.jl' % str(uuid.uuid4()),
                'CLOSESPIDER_ITEMCOUNT': max_trades
            }
        )

        #TODO: Move to own function.
        # Add the missing metadata from the TradeSpider TradeableItems.
        items = RocketLeagueGarage.get_items()
        items = {item['data_id']: item for item in items}
        for trade in trades:
            for item in trade['have'] + trade['want']:
                item_metadata = items.get(item['data_id']) or []
                item.update(item_metadata)
        return trades


    @classmethod
    def get_achievements(cls, cache_enabled: bool = True) -> List[Dict[str, Any]]:
        """Retrieve achievement data from RLG or cache.

        Args:
            cache_enabled: Get achievement data from cached webpage.

        Returns:
            A list of achievements in JSON format.

        """
        achievements = RocketLeagueGarage._run_spider(
            spider=AchievementSpider,
            settings={
                'FEED_URI': 'achievement_data_%s.jl' % str(uuid.uuid4()),
                'HTTPCACHE_ENABLED': cache_enabled,
                'HTTPCACHE_EXPIRATION_SECS': 0
            }
        )
        return achievements
