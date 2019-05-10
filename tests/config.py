"""Configuration for tests."""

import uuid
import logging

from rlgpy.scraper.spiders import (
    ItemSpider,
    TradeSpider,
    AchievementSpider
)


class Config:

    logging.basicConfig(
        filename='test_output.log',
        filemode='w',
        level=logging.DEBUG
    )

    @staticmethod
    def spider_test_info():
        yield (ItemSpider(),        {'FEED_URI': "{}.jl".format(str(uuid.uuid4())), 'FEED_FORMAT': 'jsonlines'})
        yield (TradeSpider(),       {'FEED_URI': "{}.jl".format(str(uuid.uuid4())), 'FEED_FORMAT': 'jsonlines'})
        yield (AchievementSpider(), {'FEED_URI': "{}.jl".format(str(uuid.uuid4())), 'FEED_FORMAT': 'jsonlines'})
