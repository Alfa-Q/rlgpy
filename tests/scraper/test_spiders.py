"""Test RLG spiders are functioning properly."""

import os
import json
import logging
from multiprocessing import Process
from typing import List, Any, Dict

import pytest
from twisted.internet import reactor
from scrapy.spiders import CrawlSpider
from scrapy.crawler import CrawlerRunner

from rlgpy.scraper.spiders import ItemSpider


logging.getLogger('scrapy').propagate = False


def run_spider(spider: CrawlSpider, settings: Dict[str, Any]):
    """Run spider safely.

    Prevents reactor from exploding when multiple spiders are running at once.  This function
    should be called in a separate process from other running spiders.

    Args:
        spider: The crawl spider to run.
        settings: The settings to run the spider with.

    """
    runner = CrawlerRunner(settings)
    deferred = runner.crawl(spider)
    deferred.addBoth(lambda _: reactor.stop())
    reactor.run()


@pytest.fixture(scope='function')
def scraped_file(request):
    """Represents a scraped file after the spider has been run."""

    def create_file(spider: CrawlSpider, settings: Dict[str, Any]) -> str:
        """Setup function which runs the spider specified.

        Workaround for pytest which doesn't allow arguments for fixture-wrapped functions.

        Args:
            spider: The crawl spider to run.
            settings: The settings to run the spider with.

        Returns:
            The name of the file.

        """
        filename = settings['FEED_URI']
        process = Process(target=run_spider, args=(spider, settings,))
        process.start()
        process.join()

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
    filename = scraped_file(
        spider=ItemSpider,
        settings={
            'FEED_URI': 'items.jl',
            'FEED_FORMAT': 'jsonlines'
        }
    )
    data = read_jsonlines_file(filename)
    assert len(data) > 0, 'No data retrieved.'
