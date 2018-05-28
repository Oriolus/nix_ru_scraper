import logging
from typing import Optional
from data.entities.EntityHandler import EntityHandler
from mysql.connector import MySQLConnection
from data.MySQLHelper import MySQLHelper
from data.spiders.NixSpider import NixSpider


class EntityPipeline(object):

    def __init__(self):
        self._handler = None  # type: Optional[EntityHandler]

    def process_item(self, item, spider):
        self._handler.clean_data(True)
        self._handler.insert_data(item['data'])
        self._handler.finish_process(True)

    def _get_entity_handler(self) -> EntityHandler:
        pass

    def open_spider(self, spider: NixSpider):
        self._handler = self._get_entity_handler()
        spider.set_urls(self._handler.get_urls())

    def close_spider(self, spider):
        pass
