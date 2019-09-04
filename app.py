import klein
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import config
from search.spiders.sourceCodeSpider import SourceCodeSpider
from search.utils import get_config
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from search.myCrawler import MyCrawlerRunner, return_spider_output
from search.spiders.searchSpider import SearchSpider
import json

app = Flask(__name__)

'''配置数据库'''
app.config.from_object(config['dev'])
# config['dev'].init_app(app)
db = SQLAlchemy(app)  # 实例化数据库对象，它提供访问Flask-SQLAlchemy的所有功能
db.init_app(app)


from src.com.cosmoplat.api import users


@klein.route('/getUser')
def hello_world(name):
    userList = users.getUser(name)
    print(userList)
    result = []
    for user in userList:
        result.append(user.to_json())
    return json.dumps(result, ensure_ascii=False, indent=4)


@app.route('/start')
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
    name = 'searchRule'
    runner = MyCrawlerRunner()
    spider = SearchSpider()
    deferred = runner.crawl(spider, **{'name': name})
    deferred.addCallback(return_spider_output)
    return deferred


@klein.route("/b")
def jsontest(request):
    jsonstr = "[{'title': '\r\n                            \r\n                                海尔T型冰箱(522L）\r\n                            \r\n                        ', 'url': 'http://diy.haier.com/pc/goods/detail?productId=887', 'text': '海尔全空间保鲜T型冰箱', 'website': '定制家电'}]"
    jsonstr = "{'title': '我是中国人'}"
    return json.dumps(jsonstr, ensure_ascii=False)


@klein.route("/spiders")
def spiderStart(request):
    ruleConfig = 'searchRule'
    custom_settings = get_config(ruleConfig)
    # spider = custom_settings.get('spider', 'universal')
    project_settings = get_project_settings()
    settings = dict(project_settings.copy())
    settings.update(custom_settings.get('settings'))
    runner = MyCrawlerRunner(settings)
    spider = SearchSpider(**{'ruleConfig': ruleConfig})
    deferred = runner.crawl(spider.__class__, **{'ruleConfig': ruleConfig})
    deferred.addCallback(return_spider_output)
    return deferred

@klein.route("/source")
def source(request):
    url = 'http://diy.haier.com/pc/goods/list?shopId=12'
    sourceConfig = 'source'
    custom_settings = get_config(sourceConfig)
    project_settings = get_project_settings()
    settings = dict(project_settings.copy())
    settings.update(custom_settings.get('settings'))
    runner = MyCrawlerRunner(settings)
    spider = SourceCodeSpider(**{'url': url})
    deferred = runner.crawl(spider.__class__, **{'url': url})
    deferred.addCallback(return_spider_output)
    return deferred

klein.run("localhost", 8080)

if __name__ == '__main__':
    app.run()
