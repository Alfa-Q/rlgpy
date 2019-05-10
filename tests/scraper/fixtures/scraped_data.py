"""Fixture representing list of JSON data after spider has been run."""

import logging
from typing import List, Dict, Any

import pytest

from rlgpy.scraper.runners import SafeSpiderRunner


logger = logging.getLogger(__name__)


@pytest.fixture(scope='module')
def scraped_data(request) -> List[Dict[str, Any]]:
    """Represents a scraped file data after a spider has been run.

    Only run after SafeSpiderRunner has been tested.

    Indirect Args:
        spider: The spider to run.
        settings: Dictionary containing the spider settings.

    Returns:
        A list of JSON items.

    """
    logger.info('Executing fixture "scraped_data".')
    logger.debug('Request Args: {}'.format(request.param))
    return SafeSpiderRunner.run(*request.param, True)
