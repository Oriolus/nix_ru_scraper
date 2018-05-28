import typing
import scrapy


class EntityHandler(object):

    def get_urls(self) -> typing.List[str]:
        raise NotImplementedError()

    def clean_data(self, is_deleting: bool = False):
        raise NotImplementedError()

    def insert_data(self, data):
        pass

    def finish_process(self, is_failed: bool = False):
        raise NotImplementedError()

