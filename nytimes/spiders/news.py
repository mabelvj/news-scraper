# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from nytimes.items import NewsItem, NewsLoader

script = """
function main(splash)
    local num_scrolls = 10
    assert(splash:go(splash.args.url))
    local get_dimensions = splash:jsfunc([[
        function () {
            var rect = document.getElementsByClassName('css-vsuiox')[0]
            .getElementsByTagName('button')[0]
            .getClientRects()[0];
            return {"x": rect.left, "y": rect.top};
        }
    ]])
    local scroll_to = splash:jsfunc("window.scrollTo")
    local get_body_height = splash:jsfunc(
        "function() {return document.body.scrollHeight;}"
    )
    -- Loop and click `Show More` button multiple times
    splash:set_viewport_full()
    for i=1, num_scrolls do
        scroll_to(0, get_body_height())
        splash:wait(0.5) -- to avoid errors: TypeError: null is not an object
        local dimensions = get_dimensions()
        splash:mouse_click(dimensions.x, dimensions.y)
    end
    -- Wait split second to allow event to propagate.
    splash:wait(0.1)
    return splash:html()
end
"""


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['www.nytimes.com']
    start_urls = ['http://www.nytimes.com/']

    def __init__(self, start_date="2018/01/01", end_date="2019/01/01"):
        self.urls = [self.format_query(url, start_date, end_date)
                     for url in self.start_urls]

    @staticmethod
    def format_query(url, start_date, end_date, sort='oldest'):
        """
            Params:
                start_date: string.
                    Format should be "%Y/%M/%d"
                sort: string ('oldest', 'newest', 'best')
            Example of query:

                https://www.nytimes.com/search?endDate=20190101&query=archives&sort=best&startDate=20180101
        """
        def format_date(date):
            """
            Example using datetime:
            import datetime
            datetime.datetime.strftime(
                datetime.datetime.strptime("2018/01/01", "%Y/%M/%d"),
                "%Y%M%d")"""
            return date.replace('/', '')
        start = format_date(start_date)
        end = format_date(end_date)
        sep = "/" if url[-1] != "/" else ""
        query = (url + sep +
                 "search?" +
                 "endDate=%s" % end +
                 "&query=archives&sort=%s" % sort +
                 "&startDate=%s" % start)
        return query

    def start_requests(self):
        for url in self.urls:
            print(url)
            yield SplashRequest(url, self.parse,
                                endpoint='execute',
                                args={'lua_source': script,
                                      'wait': 0.5},
                                dont_process_response=True,
                                )

    def parse(self, response, verbose=False):
        # from scrapy.shell import inspect_response
        # print(response.body)
        # inspect_response(response, self)
        entries = response.xpath('//li[@data-testid="search-bodega-result"]')

        titles = entries.xpath('//h4//text()').extract()
        types = entries.xpath('//p[@class="css-myxawk"]//text()').extract()
        dates = entries.xpath('//time//text()').extract()
        entries_text = entries.xpath('//p[@class="css-1dwgixl"]//text()'
                                     ).extract()
        if verbose:
            print('- Extracted : %s titles' % len(titles))
            print('\n', titles)
            print(types)
        for element in zip(titles, types, dates, entries_text):
            item = NewsItem(**{'title': element[0],
                               'entry_type': element[1],
                               'date': element[2],
                               'entry': element[3]})
            yield NewsLoader(item).load_item()
