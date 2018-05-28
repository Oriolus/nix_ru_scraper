from common.SpiderRunner import SpiderRunner
from data.entities.UnitEntityHandler import UnitEntityHandler
from data.spiders.UnitSpider import UnitSpider
from data.entities.PropertyEntityHandler import PropertyEntityHandler
from data.spiders.PropertySpider import PropertySpider

# SpiderRunner(UnitSpider, UnitEntityHandler).run()
SpiderRunner(PropertySpider, PropertyEntityHandler).run()
