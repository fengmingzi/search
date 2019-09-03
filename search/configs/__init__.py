
from search.utils import get_config

ruleConfig = 'searchRule'
custom_settings = get_config(ruleConfig)
item = custom_settings.get('item')
cls = eval(item.get('class'))()