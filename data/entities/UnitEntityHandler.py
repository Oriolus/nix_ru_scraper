import typing
import logging
import uuid
from mysql.connector import MySQLConnection
from data.MySQLHelper import MySQLHelper
from data.entities import EntityHandler
from data.spiders import UnitSpider
from data.dictionary import ProcessState


class UnitEntityHandler(EntityHandler):

    def __init__(self):
        self._uuid = uuid.uuid4()
        self._base_url = 'https://www.nix.ru'

    def _mark_urls(self):
        conn = None
        cnx = None  # type: typing.Optional[MySQLConnection]
        try:
            conn = MySQLHelper.connection_inst()
            conn.connect()
            query = 'update `category` set `guid` = %s where `state` in (%s, %s)'
            cnx = conn.cursor()
            cnx.execute(query, (
                str(self._uuid),
                str(ProcessState.CREATED.value),
                str(ProcessState.FAILED.value)))
            conn.commit()
        except Exception as e:
            conn.rollback()
            logging.error(e)
        finally:
            cnx = None
            if conn is not None:
                conn.close()
            conn = None

    def get_urls(self) -> typing.List[str]:

        query = 'select `url` from `category` where `guid`=%s'
        urls = []
        cnx = None
        self._mark_urls()
        conn = MySQLHelper.connection_inst()
        conn.connect()
        try:
            cnx = conn.cursor()
            cnx.execute(query, (str(self._uuid), ))
            urls = [self._base_url + row[0] for row in cnx.fetchall()]
        except Exception as e:
            logging.error(e)
        finally:
            cnx = None
            if conn is not None:
                conn.close()
            conn = None
        return urls

    def clean_data(self, is_deleting: bool = False):
        if not is_deleting:
            return
        conn = MySQLHelper.connection_inst()
        query = 'delete from `property` where `base_url` in (' \
                ' select `url` from `unit` where `state` = %s)'
        cnx = None
        try:
            cnx = conn.cursor()
            cnx.execute(query, (ProcessState.FAILED.value, ))
            query = 'delete from `unit` where state = %s'
            cnx.execute(query, (ProcessState.FAILED.value, ))
            conn.commit()
        except Exception as e:
            if conn is not None:
                conn.rollback()
            logging.error(e)
        finally:
            cnx = None
            if conn is not None:
                conn.close()
            conn = None

    def insert_data(self, data):
        conn = MySQLHelper.connection_inst()
        conn.connect()

        query = 'insert into `unit` (`base_url`, `url`, `title`)' \
                ' values (%(base_url)s, %(url)s, %(title)s)'
        cnx = None  # type: typing.Optional[MySQLConnection]
        try:
            cnx = conn.cursor()
            cnx.executemany(query, data)
            conn.commit()
        except Exception as e:
            conn.rollback()
            logging.error(e)
        finally:
            cnx = None
            conn.close()
            conn = None

    def finish_process(self, is_failed: bool = False):
        query = 'update `category` set `state` = %s where `guid` = %s'
        conn = MySQLHelper.connection_inst()
        cnx = None  # type: MySQLConnection
        try:
            cnx = conn.cursor()
            cnx.execute(
                query,
                (ProcessState.PROCESSED.value if not is_failed else ProcessState.FAILED.value,
                 str(self._uuid))
            )
            conn.commit()
        except Exception as e:
            if conn.in_transaction:
                conn.rollback()
            logging.error(e)
        finally:
            cnx = None
            if conn is not None:
                conn.close()
            conn = None
