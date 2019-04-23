"""Project item definitions."""

import scrapy
from scrapy.loader.processors import TakeFirst


class RlItem(scrapy.Item):
    """Rocket League Item representation.

    Attributes:
        data_id (int): Associated ID on Rocket League Garage.
        img_url (str): Relative URL on Rocket League Garage.
        name (str): Name of the item.
        category (str): Associated category of the item.
        platform (str): Platform that the item is on (set to All if on all platforms).
        rarity (str): Item rarity.
        dlcpack (str): The DLC pack the item is from, if applicable.

    """
    data_id = scrapy.Field(output_processor=TakeFirst(), serializer=int)
    img_url = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    category = scrapy.Field(output_processor=TakeFirst())
    platform = scrapy.Field(output_processor=TakeFirst())
    rarity = scrapy.Field(output_processor=TakeFirst())
    dlcpack = scrapy.Field(output_processor=TakeFirst())
