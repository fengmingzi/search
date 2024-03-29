from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Compose


class NewsLoader(ItemLoader):
    default_output_processor = TakeFirst()


class SearchLoader(NewsLoader):
    text_out = Compose(Join(), lambda s: s.strip())
    source_out = Compose(Join(), lambda s: s.strip())
