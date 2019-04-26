"""Rocket league item pipeline."""

from scrapy.exceptions import DropItem
from scrapy.spiders import Spider

from rlgpy.scraper.items import RlItem, RlTrade

#Normal for pipeline class... pylint: disable=too-few-public-methods
class RlItemPipeline:
    """Rocket League item data pipeline."""

    def __init__(self):
        self.item_ids = set()


    #Required argument for function... pylint: disable=unused-argument
    def process_item(self, item: RlItem, spider: Spider) -> RlItem:
        """Process item, ensuring no duplicate items are exported and setting default field values.

        Args:
            item: The loaded Rocket League item.
            spider: The spider which loaded the item.

        Raises:
            DropItem: The item has already been processed.

        Returns:
            The rocket league item.

        """
        if item['data_id'] in self.item_ids:
            raise DropItem('Item already added.')

        for field in item.fields:
            item.setdefault(field, None)

        return item


class RlTradePipeline:
    """Rocket League trade pipeline."""

    #spider is required argument for pipeline fn... pylint: disable=unused-argument
    def process_item(self, item: RlTrade, spider: Spider) -> RlTrade:
        """Set the default values for tradeable items without certifications.

        By default, tradeable items without a certification or paint or count will not have the
        keys 'certification' 'paint' or 'count'.  To normalize the data, the keys are added with
        a default value.

        """
        for tradeable_item in item['have'] + item['want']:
            tradeable_item.setdefault('count', 1)
            tradeable_item.setdefault('certification', '')
            tradeable_item.setdefault('paint', '')
        return item
