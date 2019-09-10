# -*- coding: utf-8 -*-
import json
import time
from scrapy.spiders import CrawlSpider
from scrapy_splash import SplashRequest
from search.rules import SpiderRules
from search.utils import get_config
from search import luas
from search.loaders import SearchLoader
from search.items import SearchItem


class SearchSpider(CrawlSpider):
    name = 'search_spider'
    # allowed_domains = ['search.com']
    # start_urls = ['http://search.com/']

    def __init__(self, *args, **kwargs):
        # 获取自定义的json配置文件
        config = get_config(kwargs.get('ruleConfig'))
        self.config = config

        self.startUrl = kwargs.get('startUrl')  # 入口url
        self.tenantId = kwargs.get('tenantId')
        self.indexName = kwargs.get('indexName')
        self.dataAnnotation = kwargs.get('dataAnnotation')

        self.detailUrlXpaths = kwargs.get('detailUrlXpaths')
        self.title = kwargs.get('title')
        self.content = kwargs.get('content')
        self.pageType = kwargs.get('pageType')  # 1：href，2：点击，无下一页参数，3：点击有下一页参数
        self.pageXpaths = kwargs.get('pageXpaths')  # 下一页需要的参数，json格式


        # self.pageType = 1 # 翻页类型，根据分页类型判断使用翻页方式
        # self.pageTotal = 4 # 总页数，事件点击的翻页需要配置总页数
        # self.detailUrlXpaths = '//div[@class="p-con"]/div[@class="p-box"]/ul[@class="products"]' #详情页链接xpath
        # self.pageXpaths = '//div[@id="pageStyle"]//a[contains(., "下一页")]'
        # self.selector = '.laypage_next'
        # self.attribute = 'data-page'
        # self.title = '//div[@class="pro-property"]/div[@class="pro-info"]/h2/text()'
        # self.content = '//div[@class="pro-property"]/div[@class="pro-info"]/p/text()'

        # self.rules = rules.get(config.get('rules'))
        # 根据分页类型获取rules
        if self.pageType == '1':
            pageJon = json.loads(self.pageXpaths)
            pageHrefXpath = pageJon.get('href')
            # rules配置
            self.rules = SpiderRules(detailUrlXpaths=self.detailUrlXpaths, pageXpaths=pageHrefXpath, detailCallback='parse_item', isSplash=False).rules.get('ruleHref')
        elif self.pageType == '2' or self.pageType == '3':
            self.rules = SpiderRules(detailUrlXpaths=self.detailUrlXpaths, detailCallback='parse_item').rules.get('ruleClick')

        # start_urls配置
        self.start_urls = [self.startUrl]
        # start_urls = config.get('start_urls')
        # if start_urls:
        #     if start_urls.get('type') == 'static':
        #         self.start_urls = start_urls.get('value')
        #     elif start_urls.get('type') == 'dynamic':
        #         self.start_urls = list(eval('urls.' + start_urls.get('method'))(*start_urls.get('args', [])))

        # allowed_domains配置
        # self.allowed_domains = config.get('allowed_domains')
        super(SearchSpider, self).__init__(*args, **kwargs)

    # 重写start_requests,便于对start_urls进行处理
    def start_requests(self):
        for url in self.start_urls:
            print("进入首页")
            print(url)
            yield SplashRequest(url, callback=self.parse_urls, endpoint='execute', args={'lua_source': luas.luaSimple, 'images': False})

    # 从start_requests方法回调到此方法，便于对当前列表页信息进行获取，例如获取总页数，实现分页等
    def parse_urls(self, response):
        if self.pageType == '1':  # 有fref
            # yield Request(response.url, dont_filter=True)
            yield SplashRequest(response.url, callback=self.parse, endpoint='execute', args={'lua_source': luas.luaSimple, 'images': False})
        elif self.pageType == '3':  # 有页码点击翻页
            pageJon = json.loads(self.pageXpaths)
            pageTotal = pageJon.get('totalPage')
            selector = pageJon.get('selector')
            attribute = pageJon.get('attribute')

            for page in range(1, pageTotal):
                js = "document.querySelector('{selector}').setAttribute('{attribute}',{page});document.querySelector('{selector}').click()".format(
                    selector=selector, attribute=attribute, page=page)
                yield SplashRequest(response.url, callback=self.parse, endpoint='execute', args={'lua_source': luas.luaScript, 'js': js, 'images': False})
        elif self.pageType == '2':  # 无页码点击翻页
            pageJon = json.loads(self.pageXpaths)
            selector = pageJon.get('selector')
            for page in range(1, 2):
                if page == 1:
                    yield SplashRequest(response.url, callback=self.parse, endpoint='execute', args={'lua_source': luas.luaSimple, 'images': False})
                else:
                    if page > 2:
                        break
                    js = "document.querySelector('{selector}').click()".format(selector=selector)
                    yield SplashRequest(response.url, callback=self.parse, endpoint='execute', args={'lua_source': luas.luaScript, 'js': js, 'images': False})
        else:
            pass


    # 处理Rule中增加process_request参数为splash_request的Request请求
    def splash_request(self, request, response):
        # dont_process_response=True 参数表示不更改响应对象类型（默认为：HTMLResponse；更改后为：SplashTextResponse）
        # args={'wait': 0.5} 表示传递等待参数0.5（Splash会渲染0.5s的时间）
        # meta 传递请求的当前请求的URL
        # TODO 这里需要根据定义的不同类型的lua操作来执行，例如type：1 是等待0.5s
        return SplashRequest(url=request.url, args={'wait': 0.5})

    def _requests_to_follow(self, response):
        # *************请注意我就是被注释注释掉的类型检查o(TωT)o 
        # if not isinstance(response, HtmlResponse):
        #     return
        # ************************************************
        seen = set()
        # 将Response的URL更改为我们传递下来的URL
        # 需要注意哈！ 不能直接直接改！只能通过Response.replace这个魔术方法来改！并且！！！
        # 敲黑板！！！！划重点！！！！！注意了！！！ 这货只能赋给一个新的对象（你说变量也行，怎么说都行！(*ﾟ∀ﾟ)=3）
        # newresponse = response.replace(url=response.meta.get('real_url'))
        for n, rule in enumerate(self._rules):
            # 我要长一点不然有人看不见------------------------------------newresponse 看见没！别忘了改！！！
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = self._build_request(n, link)
                yield rule.process_request(r, response)

    # 解析详情页面获取抓取的数据
    def parse_item(self, response):
        item = self.config.get('item')
        if item:
            # cls = eval(item.get('class'))()
            # loader = eval(item.get('loader'))(cls, response=response)
            loader = SearchLoader(item=SearchItem(), response=response)
            loader.add_value('tenantId', self.tenantId)
            loader.add_value('indexName', self.indexName)
            loader.add_value('dataAnnotation', self.dataAnnotation)
            # 格式化成2016-03-20 11:45:39形式
            # loader.add_value('createDate', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            loader.add_value('createDate', time.localtime())

            # 动态获取属性配置
            for key, value in item.get('attrs').items(): #attrs是json，json——>items
                for extractor in value: #value:数组，extractor：json
                    if extractor.get('method') == 'xpath':
                        args = extractor.get('args') #数组
                        if key == 'title':
                            args = [self.title]
                        elif key == 'content':
                            args = [self.content]
                        loader.add_xpath(key, *args, **{'re': extractor.get('re')})
                    if extractor.get('method') == 'css':
                        loader.add_css(key, *extractor.get('args'), **{'re': extractor.get('re')})
                    if extractor.get('method') == 'value':
                        loader.add_value(key, *extractor.get('args'), **{'re': extractor.get('re')})
                    if extractor.get('method') == 'attr':
                        loader.add_value(key, getattr(response, *extractor.get('args')))
            yield loader.load_item()
