from scrapy.http import TextResponse

from data.spiders.NixSpider import NixSpider


class CategorySpider(NixSpider):
    resource_url = ''
    name = 'Category'

    custom_settings = {
        'ITEM_PIPELINES':
            {
                'pipelines.CategoryPipeline.CategoryPipeline': 100
            }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def parse(self, response: TextResponse):
        categories = []
        base_url = response.url
        for index, item in enumerate(response.css('ul.nix-menu').xpath('li')):
            url = item.css('a::attr(href)').extract_first()
            title = item.css('a::text').extract_first()
            categories.append({
                'base_url': base_url,
                'url': url,
                'title': title
            })
        return {'data': categories}
