from scrapy.crawler import CrawlerProcess
from data.entities.EntityHandler import EntityHandler


class SpiderRunner(object):

    def __init__(self, spider, entity: EntityHandler):
        self._spider = spider
        self._entity = entity
        pass

    def run(self):
        cp = CrawlerProcess()
        cp.crawl(
            self._spider
        )
        cp.start()
        cp.join()
