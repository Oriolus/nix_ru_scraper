from scrapy import FormRequest
from scrapy.http import TextResponse
from scrapy import Request
import json

from data.spiders import NixSpider


class UnitSpider(NixSpider):
    resource_url = ''
    name = 'Property'
    api_url = 'https://www.nix.ru/lib/fast_search.php'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    custom_settings = {
        'ITEM_PIPELINES': {
            'data.pipelines.UnitPipeline.UnitPipeline': 100
        }
    }

    def parse(self, response: TextResponse):
        input_hidden = response.css('input[type="hidden"]')
        form_data = {
            'command': 'get_goods',
            'page': 'all',
            'store': 'msk-0_1721_1',
            'thumbnail_view': '2',
            'sch_good_id': '',
            'sch_id': '',
            'c_id': input_hidden.css('input[name="c_id"]::attr(value)').extract_first(),
            'fn': input_hidden.css('input[name="fn"]::attr(value)').extract_first(),
            'g_id': input_hidden.css('input[name="g_id"]::attr(value)').extract_first(),
            'def_sort': input_hidden.css('input[name="def_sort"]::attr(value)').extract_first(),
            'sys_all': input_hidden.css('input[name="sys_all"]::attr(value)').extract_first()
        }
        return FormRequest(self.api_url, headers={'user_base_url': response.url}, formdata=form_data, callback=self.parse_unit)

    def parse_unit(self, response: TextResponse):
        resp = TextResponse(
            url=response.url,
            request=response.url,
            body=json.loads(response.body.decode('utf-8'))['goods']['html'],
            encoding='utf-8'
        )
        base_url = response.request.headers['user_base_url']
        units = []
        for index, item in enumerate(resp.css('table#search_results tr.highlight')
                                             + resp.css('table#search_results tr.editors_choise')):
            url = self.strip(item.css('a.t::attr(href)').extract_first())
            title = self.strip(item.css('a.t span::text').extract_first())
            units.append({
                'base_url': base_url,
                'url': url,
                'title': title
            })
        return {'data': units}
