from scrapy.http import TextResponse
from data.spiders.NixSpider import NixSpider


class PropertySpider(NixSpider):

    name = 'Property'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    custom_settings = {
        'ITEM_PIPELINES': {
            'data.pipelines.PropertyPipeline.PropertyPipeline': 100
        }
    }

    def parse(self, response: TextResponse):
        base_url = response.url
        properties = []
        for index, item in enumerate(response.css('table#PriceTable tr')):
            own_id = self.strip(item.css('td::attr(id)').extract_first())
            params = item.css('td::text').extract()
            key = None
            value = None
            if len(params) > 0:
                key = self.strip(params[0])
            if len(params) > 1:
                value = self.strip(params[1])
            properties.append({
                'base_url': base_url,
                'own_id': own_id,
                'key': key,
                'value': value
            })
        return {'data': properties}
