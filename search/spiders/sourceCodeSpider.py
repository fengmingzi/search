from scrapy.spiders import CrawlSpider
from scrapy_splash import SplashRequest

from search import luas
from search.items import SourceItem
from search.loaders import SearchLoader


class SourceCodeSpider(CrawlSpider):
    name = 'source_code_spider'
    # allowed_domains = ['search.com']
    # start_urls = ['http://search.com/']

    def __init__(self, *args, **kwargs):
        # start_urls配置
        start_urls = [kwargs.get('url')]
        if start_urls:
            self.start_urls = start_urls

        # allowed_domains配置
        # self.allowed_domains = config.get('allowed_domains')
        super(SourceCodeSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            print("进入首页")
            print(url)
            yield SplashRequest(url, callback=self.parse_item, endpoint='execute', args={'lua_source': luas.luaSimple, 'images': False})


    def parse_item(self, response):
        print(response.text)
        loader = SearchLoader(item=SourceItem(), response=response)
        loader.add_value('source', getattr(response, 'text'))
        yield loader.load_item()
