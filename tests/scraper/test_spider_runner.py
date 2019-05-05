"""Test spider runners."""

import logging

import pytest

from tests.config import Config
from rlgpy.scraper.runners import SafeSpiderRunner


logger = logging.getLogger(__name__)


@pytest.mark.integration
@pytest.mark.parametrize(
    argnames='spider,settings',
    argvalues=[test for test in Config.spider_test_info()],
    scope='module'
)
def test_runner_single_no_errors(spider, settings):
    """Ensure the custom spider runner will run synchronously without producing any errors."""
    logger.info('Testing spider runner for {}'.format(spider))
    SafeSpiderRunner.run(spider=spider, settings=settings, delete_file=True)
