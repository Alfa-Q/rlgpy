"""Rocket league item pipeline."""

from scrapy.exceptions import DropItem
from scrapy.spiders import Spider

from scraper.items import RlItem

#Normal for pipeline class... pylint: disable=too-few-public-methods
class RlItemPipeline:
    """Rocket League item data pipeline."""

    def __init__(self):
        self.item_ids = set()

    #spider is required argument for pipeline fn... pylint: disable=unused-argument
    def process_item(self, item: RlItem, spider: Spider) -> RlItem:
        """Ensure no duplicate items are exported and set default field values."""

        if item['data_id'] in self.item_ids:
            raise DropItem('Item already added.')

        self.item_ids.add(item['data_id'])

        for field in item.fields:
            item.setdefault(field, None)

        return item
