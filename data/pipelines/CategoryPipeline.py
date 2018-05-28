import logging
from mysql.connector import MySQLConnection
from data.MySQLHelper import MySQLHelper


class CategoryPipeline(object):

    def __init__(self):
        self._insert_query = 'insert into category (base_url, url, `title`)' \
                             ' values (%(base_url)s, %(url)s, %(title)s)'
        self._connection = None

    def process_item(self, item, spider):
        self._connection = MySQLHelper.get_instance().get_connection()  # type: MySQLConnection
        cnx = None
        try:
            self._connection.connect()
            cnx = self._connection.cursor()
            cnx.executemany(self._insert_query, item['data'])
            self._connection.commit()
        except Exception as e:
            self._connection.rollback()
            logging.error(e)
        finally:
            cnx = None
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self._connection = None
