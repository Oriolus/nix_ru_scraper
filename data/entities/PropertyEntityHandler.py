import typing
import logging
import uuid
from mysql.connector import MySQLConnection
from data.MySQLHelper import MySQLHelper
from data.entities import EntityHandler
from data.spiders import UnitSpider
from data.dictionary import ProcessState


class PropertyEntityHandler(EntityHandler):

    def __init__(self):
        self._uuid = uuid.uuid4()
        self._base_url = 'https://www.nix.ru'

    def _mark_urls(self):
        conn = MySQLHelper.connection_inst()
        conn.connect()
        cnx = None
        try:
            query = 'update `unit` set `guid` = %s ' \
                    ' where `state` = %s'
            cnx = conn.cursor()
            cnx.execute(query, (
                str(self._uuid),
                ProcessState.CREATED.value,)
            )
            conn.commit()
        except Exception as e:
            if conn.in_transaction:
                conn.rollback()
            logging.error(e)
        finally:
            cnx = None
            conn.close()
            conn = None

    def get_urls(self) -> typing.List[str]:

        self._mark_urls()
        conn = MySQLHelper.connection_inst()
        conn.connect()
        cnx = None
        urls = []
        query = 'select `url` from `unit` where `guid` = %s'

        try:
            cnx = conn.cursor()
            cnx.execute(query, (str(self._uuid), ))
            urls = [self._base_url + row[0] for row in cnx.fetchall()]
        except Exception as e:
            logging.error(e)
        finally:
            cnx = None
            conn.close()
            conn = None
        return urls

    def finish_process(self, is_failed: bool = False):
        if is_failed:
            return

        conn = MySQLHelper.connection_inst()
        conn.connect()
        cnx = None
        query = 'update `property` set' \
                ' `state` = %s,' \
                ' `guid` = NULL,' \
                ' where `guid` = %s'
        try:
            cnx = conn.cursor()
            cnx.execute(query, (
                ProcessState.PROCESSED.value,
                str(self._uuid))
            )
            conn.commit()
        except Exception as e:
            if conn.in_transaction:
                conn.rollback()
            logging.error(e)
        finally:
            cnx = None
            conn.close()
            conn = None

    def insert_data(self, data):
        conn = MySQLHelper.connection_inst()
        conn.connect()
        cnx = None
        query = 'insert into ' \
                ' `property` (`base_url`, `own_id`, `key`, `value`) ' \
                ' values(%(base_url)s, %(own_id)s, %(key)s, %(value)s)'

        try:
            cnx = conn.cursor()
            cnx.executemany(query, data)
            conn.commit()
        except Exception as e:
            if conn.in_transaction:
                conn.rollback()
            logging.error(e)
        finally:
            cnx = None
            conn.close()
            conn = None

    def clean_data(self, is_deleting: bool = False):
        if not is_deleting:
            return
        return

