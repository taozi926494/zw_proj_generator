# -*- coding: utf-8 -*-

import scrapy

from ..utils import name_generator
from ..utils.catelogs import catelogs
from ..items import PaperListItem
from ..utils.parse_err import log, NO_REQUIRED, NO_LIST


class MasterSpider(scrapy.Spider):
    # 从setting.py中获取工程名，并在工程名后面加上 自定义标识后缀 作为爬虫名
    name = name_generator.spidername_master()
    '''
    由于翻页规则为：index, index_1, index_2 ...,
    先提取第一页的列表数据, 再增加页码提取之后的列表数据
    这里定义一个首页标识
    '''
    first_page = True
    main_page = 'http://www.beijing.gov.cn'

    def start_requests(self):
        """
        发起首页请求
        :return: yield Request
        """
        for catelog in catelogs:
            yield scrapy.Request(url=catelog.pop('url'), meta=catelog, callback=self.parse_list)

    def parse_list(self, response):
        """
        处理响应，提取列表页数据的页面
        :param response: HttpResponse response
        :return: yield PaperListItem or Request
        """
        meta = response.meta
        paper_list = response.xpath(meta['extract_code'])
        if not paper_list:
            log(NO_LIST, 'paper_list', '公文列表', response)

        paperlistItem = PaperListItem()
        paperlistItem['paper_list'] = []
        for paper in paper_list:
            paper_item = {}
            paper_item['url'] = paper.xpath('a/@href').extract_first()
            if paper_item['url']:
                paper_item['url'] = self.main_page + paper_item['url']
            else:
                log(NO_REQUIRED, 'paper_url', '公文url地址', response)
                return

            paper_item['title'] = paper.xpath('a/text()').extract_first()
            paper_item['reference_number_info'] = paper.xpath('span/text()').extract_first()
            paper_item['sign'] = meta['sign']
            paper_item['sec_title'] = meta['sec_title']
            paperlistItem['paper_list'].append(paper_item)
        yield paperlistItem

        # 提取翻页信息
        next_page = response.xpath('//div[@class="fy"]/a[contains(text(), "下一页")]/@href').extract_first()
        if next_page:
            next_page = self.main_page + next_page
            yield scrapy.Request(url=next_page, meta=meta, callback=self.parse_list)
