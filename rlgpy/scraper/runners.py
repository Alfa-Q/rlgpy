"""Custom spider runner."""

import logging
import json
from pathlib import Path
from typing import List, Dict, Any
from multiprocess import Process

from twisted.internet import reactor
from scrapy.spiders import Spider
from scrapy.crawler import CrawlerRunner


logger = logging.getLogger(__name__)


class SafeSpiderRunner:
    """Runs a spider with the specified settings synchronously."""


    @staticmethod
    def _crawl_safely(spider: Spider, settings: Dict[str, Any]):
        """Run a scrapy spider safely.

        Prevents reactor from exploding when multiple spiders are running at once.  This function
        should be called in a separate process from other running spiders.

        Args:
            spider: The scrapy spider to run.
            settings: The settings to run the spider with.

        """
        runner = CrawlerRunner(settings)
        deferred = runner.crawl(spider)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()


    @staticmethod
    def _get_results(filepath: str, delete_file: bool) -> List[Dict[str, Any]]:
        """Retrieve results from file.

        Args:
            filepath: The filepath of the jsonlines file.
            delete_file: Remove the file.

        """
        logger.info('Getting results from file %s' % filepath)
        filepath = Path(filepath)
        filedata = [json.loads(line) for line in filepath.read_text().splitlines()]
        if delete_file:
            logger.info('Unlinking filepath %s' % filepath)
            filepath.unlink()
        return filedata


    @staticmethod
    def run(spider: Spider, settings: Dict[str, Any], delete_file: bool) -> List[Dict[str, Any]]:
        """Run the spider until done, a blocking function.

        Args:
            spider: Spider to run.
            settings: Spider settings.
            delete_file: Delete the file after getting the results.

        Returns:
            A list of the json data.

        """
        logger.info('Creating new process for spider %s' % spider)
        p = Process(target=SafeSpiderRunner._crawl_safely, args=(spider, settings,))
        p.start()
        p.join()
        logger.info('%s finished running' % spider)
        results = SafeSpiderRunner._get_results(settings['FEED_URI'], delete_file)
        logger.debug('%d items retrieved' % len(results))
        return results
