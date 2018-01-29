#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from items import LagouJobItemLoader, LagouJobItem
from utils.common import get_md5

class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    cookie = '_ga=GA1.2.346165727.1515229724; user_trace_token=20180106170851-366042b6-f2c1-11e7-bfae-525400f775ce; LGUID=20180106170851-36604969-f2c1-11e7-bfae-525400f775ce; _ga=GA1.3.346165727.1515229724; index_location_city=%E5%85%A8%E5%9B%BD; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1515229724,1515399646,1515404057,1517040195; _gat=1; _gid=GA1.2.1140833278.1517040195; JSESSIONID=ABAAABAABFGAAIF449797AE06D7B12E013EF3C0E26D1DDB; LGSID=20180127160322-8b109727-0338-11e8-9d30-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; X_HTTP_TOKEN=23f7b4580550f10d22e44f743010ccfe; TG-TRACK-CODE=undefined; gate_login_token=f34202f8d9876b3bb0f3bc090ee5957882fe44de98a99707; login=false; unick=""; _putrc=""; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1517040715; LGRID=20180127161201-c0cee875-0339-11e8-9d30-525400f775ce'

    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 2,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': cookie,
            'Host': 'www.lagou.com',
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
    }


    rules = (
        Rule(LinkExtractor(allow=('zhaopin/.*',)), ),
        Rule(LinkExtractor(allow=('gongsi/j\d+.html',)), ),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
    )

    def parse_job(self, response):
        """
        解析拉勾网的职位
        """
        item_loader = LagouJobItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_css("title", ".job-name::attr(title)")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("salary", ".job_request .salary::text")
        item_loader.add_xpath("job_city", "//*[@class='job_request']/p/span[2]/text()")
        item_loader.add_xpath("work_years", "//*[@class='job_request']/p/span[3]/text()")
        item_loader.add_xpath("degree_need", "//*[@class='job_request']/p/span[4]/text()")
        item_loader.add_xpath("job_type", "//*[@class='job_request']/p/span[5]/text()")
        item_loader.add_css("publish_time", ".publish_time::text")
        item_loader.add_css("job_advantage", ".job-advantage p::text")
        item_loader.add_css("company_name", "#job_company dt a img::attr(alt)")
        item_loader.add_css("company_url", "#job_company dt a::attr(href)")
        item_loader.add_css("tags", ".position-label li::text")


        job_item = item_loader.load_item()

        yield job_item
