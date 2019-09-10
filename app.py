from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import config
from search.spiders.sourceCodeSpider import SourceCodeSpider
from search.utils import get_config
from scrapy.utils.project import get_project_settings
from search.myCrawler import MyCrawlerRunner, return_spider_output
from search.spiders.searchSpider import SearchSpider
import json
from flask_twisted import Twisted
import klein

app = Flask(__name__)

'''配置数据库'''
app.config.from_object(config['dev'])
# config['dev'].init_app(app)
db = SQLAlchemy(app)  # 实例化数据库对象，它提供访问Flask-SQLAlchemy的所有功能
db.init_app(app)

from src.com.cosmoplat.api import usersService
from src.com.cosmoplat.api import tenantRulesService


@klein.route('/getRules')
def getRules(request):
    tenantRules = tenantRulesService.findAll()
    print(tenantRules)
    result = []
    for tenantRule in tenantRules:
        print(tenantRule.category_name)
        result.append(tenantRule.to_json())
    return json.dumps(result, ensure_ascii=False, indent=4)


@klein.route('/start')
def start():
    # name = sys.argv[1] # json配置文件的名称
    # name = 'searchRule'
    # custom_settings = get_config(name)
    # spider = custom_settings.get('spider', 'universal')
    # project_settings = get_project_settings()
    # settings = dict(project_settings.copy())
    # settings.update(custom_settings.get('settings'))
    # process = CrawlerProcess(settings)
    # process.crawl(spider, **{'name': name})  # 第一个参数spider是要启动的爬虫类名，第二个参数：**{'name': name}是universal类中init初始化方法中name参数
    # process.start()
    # print('执行结束')
    return ""


@klein.route("/spiders")
def spiderStart(request):
    ruleConfig = 'searchRule'
    custom_settings = get_config(ruleConfig)
    # spider = custom_settings.get('spider', 'universal')
    project_settings = get_project_settings()
    settings = dict(project_settings.copy())
    settings.update(custom_settings.get('settings'))
    runner = MyCrawlerRunner(settings)
    tenantRules = tenantRulesService.findAll()
    print(tenantRules)
    for tenantRule in tenantRules:
        pamJson = {'ruleConfig': ruleConfig,    # 规则配置文件名称
                   'tenantId': tenantRule.tenant_id,  # 租户id
                   'indexName': tenantRule.index_name,  # 索引名称
                   'dataAnnotation': tenantRule.dictionary_data_annotation,  # 数据标注
                   'startUrl': tenantRule.list_url,  # 入口url
                   'detailUrlXpaths': tenantRule.detail_page_url_xpath,  # 详情页url的xpath
                   'pageType': tenantRule.dictionary_next_page_type,    # 下一页类型
                   'pageXpaths': tenantRule.next_page_xpath,    # 下一页需要的参数json，根据类型json不同，详见实体类
                   'title': tenantRule.detail_title_xpath,  # 详情页标题xpath
                   'content': tenantRule.detail_content_xpath   # 详情页内容xpath
                   }
        # self.pageType = 1  # 翻页类型，根据分页类型判断使用翻页方式
        # self.pageTotal = 4  # 总页数，事件点击的翻页需要配置总页数
        # self.detailUrlXpaths = '//div[@class="p-con"]/div[@class="p-box"]/ul[@class="products"]'  # 详情页链接xpath
        # self.pageXpaths = '//div[@id="pageStyle"]//a[contains(., "下一页")]'
        # self.selector = '.laypage_next'
        # self.attribute = 'data-page'
        # self.title = '//div[@class="pro-property"]/div[@class="pro-info"]/h2/text()'
        # self.content = '//div[@class="pro-property"]/div[@class="pro-info"]/p/text()'
        # {"pageTotal": 4, "selector": ".laypage_next", "attribute": "data-page"}

        # spider = SearchSpider(**{'ruleConfig': ruleConfig})
        deferred = runner.crawl(SearchSpider, **pamJson)
        # deferred.addCallback(return_spider_output)
    return 'ok'


@klein.route('/source', methods=['POST'])
def source(request):
    # name = request.form.get("name")
    #
    # age = request.form.get("age")
    #
    # name_li = request.form.getlist("name")
    #
    # # 如果是请求体的数据不是表单格式的（如json格式），可以通过request.data获取
    #
    # print("request.data: %s" % request.data)
    #
    # # args是用来提取url中的参数（查询字符串）
    #
    # url = request.args.get("url")
    # url = 'http://diy.haier.com/pc/goods/list?shopId=12'
    content = json.loads(request.content.read())
    print(content['url'])
    url = content['url']
    sourceConfig = 'source'
    custom_settings = get_config(sourceConfig)
    project_settings = get_project_settings()
    settings = dict(project_settings.copy())
    settings.update(custom_settings.get('settings'))
    runner = MyCrawlerRunner(settings)
    # spider = SourceCodeSpider(**{'url': url})
    deferred = runner.crawl(SourceCodeSpider, **{'url': url})
    deferred.addCallback(return_spider_output)
    return deferred


@klein.route('/pam/<name>')
def pam(request, name):
    # request.get('name')
    # name = request.args.get("name")
    return name


@klein.route('/cc', methods=['POST'])
def do_post(request):
    content = json.loads(request.content.read())
    print(content['url'])
    response = json.dumps(content, indent=4)
    print(response['url'])
    return response


@klein.route('/testget/<path:catchall>')
def setname(request, catchall):
    # name = request.args.get('name')
    # content = json.loads(request.args)
    # print(content)
    # <class 'dict'>: {b'name': [b'http://127.0.0.1:8080/testget']}
    name = request.args.get('name')
    print(name)
    dd = dict(request.args.get('name'))
    print(dd['name'])
    aa = convert(dd)
    print(aa)
    json.dumps(aa, ensure_ascii=False)
    return json


def convert(data):
    if isinstance(data, bytes):  return data.decode('ascii')
    if isinstance(data, dict):   return dict(map(convert, data.items()))
    if isinstance(data, tuple):  return map(convert, data)
    return data


@klein.route('/getUser')
def getname(request):
    userList = usersService.getUser('jj')
    print(userList)
    for user in userList:
        print(user.content)
        j = json.loads(user.content)
        print(j.get('name'))
    return 'ok'


klein.run("localhost", 8080)
if __name__ == '__main__':
    app.run()
