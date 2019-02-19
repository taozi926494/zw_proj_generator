# -*- coding: utf-8 -*-
from urllib.parse import urlparse

import scrapy

from ..utils import name_generator
from ..utils.catelogs import catelogs
from ..items import PaperListItem
from ..utils.parse_err import log, NO_REQUIRED, NO_LIST
from ..utils import data_operator


class MasterSpider(scrapy.Spider):
    # 从setting.py中获取工程名，并在工程名后面加上 自定义标识后缀 作为爬虫名
    name = name_generator.spidername_master()


    def start_requests(self):
        """
        发起首页请求
        :return: yield Request
        """
        for catelog in catelogs:
            '''
            某些翻页规则为：index, index_1, index_2 ...,
            先提取第一页的列表数据, 再增加页码提取之后的列表数据
            这里定义一个首页标识
            '''
            # catelog['first_page'] = True

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
            paper_url = paper.xpath('a/@href').extract_first()
            if paper_url:
                paper_url = data_operator.unify_url(paper_url, response)
                # 提取到的url与主页的url应该在同一个域名下, 而不是跳转到其他的网址
                if urlparse(paper_url).netloc == urlparse(response.url).netloc:
                    paper_item['url'] = paper_url
                else:
                    continue
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
        # [** NOTICE **] 注意修改xpath页码部分的提取规则
        # [** NOTICE **] 同时注意浏览最后一页的a标签href规则，某些网站最后一页是javascript(void(0))或者就是最后一页的地址
        #     不在下方做判断会造成重复翻页
        next_page = response.xpath('//div[@class="fy"]//a[contains(text(), "下一页")]/@href').extract_first()
        if next_page:
            next_page = data_operator.unify_url(next_page, response)
            yield scrapy.Request(url=next_page, meta=meta, callback=self.parse_list)
