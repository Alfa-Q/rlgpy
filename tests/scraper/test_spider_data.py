"""Test the integrity of the spider data being retrieved.

Each spiders should retrieve some amount of data form the default URL.

Note:
    The scraped_data fixture ensure that all integration tests will only make a request once per
    spider, significantly improving testing speed.

"""

import logging

import pytest

from tests.scraper.fixtures import scraped_data  # pylint: disable=unused-import
from tests.config import Config


logger = logging.getLogger(__name__)


@pytest.mark.integration
@pytest.mark.parametrize(
    argnames='scraped_data',
    argvalues=[test for test in Config.spider_test_info()],
    indirect=True
)
def test_spider_data_not_null(scraped_data):
    """Test the spiders are functioning."""
    logger.debug('Scraped data id: {}'.format(id(scraped_data)))
    logger.debug('Scraped data type: {}'.format(type(scraped_data)))
    assert scraped_data != None, 'File data was null!\nExpected type: List[Dict[str, Any]]'


@pytest.mark.integration
@pytest.mark.parametrize(
    argnames='scraped_data',
    argvalues=[test for test in Config.spider_test_info()],
    indirect=True
)
def test_spider_data_not_empty(scraped_data):
    """Test the spider retrieves at least one data item."""
    logger.debug('Scraped data id: {}'.format(id(scraped_data)))
    logger.debug('Scraped data type: {}'.format(type(scraped_data)))
    assert len(scraped_data) > 0, "No data was retrieved!"
