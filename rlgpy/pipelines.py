"""Rocket league item pipeline."""

from scrapy.exceptions import DropItem
from scrapy.spiders import Spider

from rlgpy.items import RlItem

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
