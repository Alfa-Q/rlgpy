"""Project item definitions.

#TODO: Change relative URL to absolute URL of image resources.

"""

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Compose, Identity


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

    data_id = scrapy.Field()
    img_url = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    platform = scrapy.Field()
    rarity = scrapy.Field()
    dlcpack = scrapy.Field()


class RlItemLoader(ItemLoader):
    """Item loader for RlItem."""

    default_output_processor = TakeFirst()
    data_id_out = Compose(lambda v: v[0], int)


class RlTradeableItem(scrapy.Item):
    """Rocket League tradeable item representation.

    Does not contain the item meta-data associated with the data_id.

    Attributes:
        data_id (int): Associated ID on RLG.
        count (int): Total number of the item.
        certification (str): The type of certification, if any.
        paint (str): The paint type, if any.

    """

    data_id = scrapy.Field()
    count = scrapy.Field()
    certification = scrapy.Field()
    paint = scrapy.Field()


class RlTradeableItemLoader(ItemLoader):
    """Item loader for a RlTradeableItem."""

    default_output_processor = TakeFirst()
    data_id_out = Compose(lambda v: v[0], int)
    count_out = Compose(lambda v: v[0], int)


class RlTrade(scrapy.Item):
    """Rocket League Trade representation.

    Attributes:
        data_id (str): The unique ID of the trade on RLG.
        url (str): Relative URL of the trade on RLG.
        rlg_username (str): Author's RLG site username.
        platform (str): Platform of the trade.
        have (List[RlTradeableItem]): List of items the author has.
        want (List[RlTradeableItem]): List of items the author wants.

    """

    data_id = scrapy.Field()
    url = scrapy.Field()
    rlg_username = scrapy.Field()
    platform = scrapy.Field()
    have = scrapy.Field()
    want = scrapy.Field()


class RlTradeLoader(ItemLoader):
    """Item loader for a RlTrade."""

    default_output_processor = TakeFirst()
    platform_out = Compose(lambda x: x[0], str.upper)
    have_out = Identity()
    want_out = Identity()


class RlAchievement(scrapy.Item):
    """Rocket League Achievement representation.

    Attributes:
        name (str): Achievement name.
        img_url (str): Relative URL of the achievement image.
        gamerscore (int): The achievement's gamerscore on XBOX platform.
        trophy_type (str): The trophy on the PSN platform.
        description (str): Achievement description.

    """

    name = scrapy.Field()
    img_url = scrapy.Field()
    gamerscore = scrapy.Field()
    trophy_type = scrapy.Field()
    description = scrapy.Field()


class RlAchievementLoader(ItemLoader):
    """Achievement loader for a RlAchievement."""

    default_output_processor = TakeFirst()
    gamerscore_out = Compose(lambda v: v[0], int)
    trophy_type_out = Compose(lambda v: v[0], str.upper)
