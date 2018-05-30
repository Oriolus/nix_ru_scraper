from common import SpiderRunner
from data.entities import UnitEntityHandler, PropertyEntityHandler
from data.spiders import UnitSpider, PropertySpider

# SpiderRunner(UnitSpider, UnitEntityHandler).run()
SpiderRunner(PropertySpider, PropertyEntityHandler).run()
