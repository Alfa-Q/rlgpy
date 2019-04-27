"""Test RLG spiders are functioning properly."""

import os
import json
import logging
from typing import List, Any, Dict

import pytest
from scrapy.spiders import CrawlSpider
from scrapy.crawler import CrawlerProcess

from rlgpy.scraper.spiders import ItemSpider, TradeSpider


logging.getLogger('scrapy').propagate = False


@pytest.fixture(scope='function')
def scraped_file(request):
    """Represents a scraped file after the spider has been run."""

    def create_file(spider: CrawlSpider, filename: str) -> str:
        """Setup function which runs the spider specified.

        Workaround for pytest which doesn't allow arguments for fixture-wrapped functions.

        Args:
            spider: The spider to run.
            filename: The file to save the data scraped by the spider.

        Returns:
            The name of the file.

        """
        process = CrawlerProcess({
            'FEED_URI': filename,
            'FEED_FORMAT': 'jsonlines'
        })
        process.crawl(spider)
        process.start()

        def teardown():
            """Remove the scraped file."""
            print(f"Removing scraped file '{filename}'")
            os.remove(filename)
            assert not os.path.exists(filename)
            print("File successfully removed.")

        request.addfinalizer(teardown)
        return filename

    return create_file


def read_jsonlines_file(filepath: str) -> List[Dict[str, Any]]:
    """Get jsonlines file data.

    Helper function used after the spider is done crawling.

    Args:
        filepath: The filepath of the jsonlines file.

    Returns:
        A list of JSON data.

    """
    data = list()
    with open(filepath, 'r') as jsonlines_file:
        data = [json.loads(line) for line in jsonlines_file.readlines()]
    return data


# Pytest magic... pylint: disable=redefined-outer-name
def test_item_spider(scraped_file):
    """Testing that the item spider works correctly."""
    filename = scraped_file(spider=ItemSpider, filename='items.jl')
    data = read_jsonlines_file(filename)
    assert len(data) > 0, 'No data retrieved.'
