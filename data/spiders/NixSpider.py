import scrapy
from scrapy.http import TextResponse
from typing import Optional, List


class NixSpider(scrapy.Spider):

    name = ''
    start_urls = None

    def __init__(self, **kwargs):
        super().__init__(self.name, **kwargs)
        self._pre_init(**kwargs)
        self._init_kwargs(**kwargs)
        self.resource_url = 'https://www.nix.ru'

    def _pre_init(self, **kwargs):
        if 'urls' in kwargs:
            self.start_urls = kwargs['urls'] or []

    def _init_kwargs(self, **kwargs):
        pass

    def strip(self, value) -> Optional[str]:
        if value is None:
            return value
        return str(value).strip()

    def set_urls(self, urls: List[str]):
        self.start_urls = urls

    def parse(self, response: TextResponse):
        pass
