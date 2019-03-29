# -*- coding: utf-8 -*-
import datetime
import re

import scrapy
from scrapy.utils.project import get_project_settings

import json
from scrapy_redis.utils import bytes_to_str
from scrapy_redis.spiders import RedisSpider

from ..utils import name_generator, data_operator
from ..utils.snow import Snow

from ..items import PaperItem


class SlaveSpider(RedisSpider):
    name = name_generator.spidername_slave()
    redis_key = name_generator.redis_collection()
    snow = Snow()
    source = get_project_settings().get('SECTION_SOURCE')

    def make_request_from_data(self, data):
        """
        重写RedisCrawlSpider中的该算法, 以实现更多参数的传递
        :param data: redis数据库中获取的数据
            data = {
                'url': '详情页url',
                'title': '文章标题',
                'sec_title': '所属分类标题',
                'reference_number_info': '列表页提取的文号',
                'sign': '该文章的一些自定义标识（如：3年前：old， 近三年：new）',
            }
        :return:
        """
        redis_data = json.loads(bytes_to_str(data, self.redis_encoding))
        url = redis_data.pop('url')
        redis_data['is_attach'] = data_operator.is_attachment(url)
        return scrapy.Request(url=url, callback=self.parse_paperpage, meta=redis_data)

    def parse_paperpage(self, response):
        """
        获取公文详情页的信息
        :param response: 公文详情页的response
        :return: yield ParperItem 公文信息Item
        :param response:
        :return:
        """
        # 以下为基本信息, 勿修改
        meta = response.meta
        paper_item = PaperItem()
        # [** NOTICE **] 勿修改，赋值item的必填基础字段 _id, url, source, sec_title, insert_date, update_date
        self.required_field(response, paper_item)

        # 如果不是附件
        if not meta['is_attach']:
            paper_item['source_html'] = response.xpath('/html').extract_first()  # 网页源码
            # 信息盒区域
            info_box = response.xpath('*//ol[@class="doc-info"]')
            if info_box:
                paper_item['topic_cat_info_alias'] = '主题分类'
                paper_item['topic_cat_info'] = self.extract_boxitem(info_box, '主题分类')

                paper_item['pub_office_info_alias'] = '发文机构'
                paper_item['pub_office_info'] = self.extract_boxitem(info_box, '发文机构')

                paper_item['draft_date_info_alias'] = '成文日期'
                paper_item['draft_date_info'] = data_operator.unify_date(self.extract_boxitem(info_box, '成文日期'))
                # 如果没有提取到成文日期, 就从正文中去找
                if not paper_item['draft_date_info']:
                    textlines = response.xpath('*//div[@id="textBox"]/p/text()').extract()
                    paper_item['draft_date_info'] = data_operator.unify_date(
                        data_operator.draftdate_from_textlines(textlines))

                # [** NOTICE **] 一般列表页都有文号或者发布日期，会在主爬虫里push到redis中
                # 这里增加一个从列表页获取文号或者发布日期（这段代码可以不用修改，获取不到就为None）
                paper_item['pub_date_info_alias'] = '发布日期'
                paper_item['pub_date_info'] = data_operator.unify_date(self.extract_boxitem(info_box, '发布日期'))
                if not paper_item['pub_date_info']:
                    paper_item['pub_date_info'] = meta.get('pub_date_info')

                paper_item['reference_number_info_alias'] = '发文字号'
                paper_item['reference_number_info'] = self.extract_boxitem(info_box, '发文字号')
                if not paper_item['reference_number_info']:
                    paper_item['reference_number_info'] = meta.get('reference_number_info')

                paper_item['effective_date_info_alias'] = '实施日期'
                paper_item['effective_date_info'] = data_operator.unify_date(self.extract_boxitem(info_box, '实施日期'))

                paper_item['expire_date_info_alias'] = '废止日期'
                paper_item['expire_date_info'] = data_operator.unify_date(self.extract_boxitem(info_box, '废止日期'))

            # 标题
            paper_item['title'] = response.xpath('*//div[@class="doc-header"]/h1/text()').extract_first()
            paper_item['title'] = paper_item['title'].strip() if paper_item['title'] else meta['title']
            # 正文
            paper_item['text'] = response.xpath('*//div[@id="textBox"]').xpath('string(.)').extract_first()
            # 正文源码
            paper_item['text_html'] = response.xpath('*//div[@id="textBox"]').extract_first()
            # 附件
            # [** NOTICE **] 注意附件的提取规则
            attachments = response.xpath('*//div[@id="textBox"]//a/@href').extract()
            if attachments:
                paper_item['attachment'] = data_operator.extract_attachments(
                    attachments, response, attach_has_postfix=True)

        else:
            # 如果是附件
            self.attach_field(response, paper_item)
            # [** NOTICE **] 一般列表页都有文号或者发布日期，会在主爬虫里push到redis中
            # 这里增加一个从列表页获取文号或者发布日期（这段代码可以不用修改，获取不到就为None）
            paper_item['reference_number_info'] = meta.get('reference_number_info')
            paper_item['pub_date_info'] = meta.get('pub_date_info')

        yield paper_item

    def required_field(self, response, item):
        """
        必填字段
        :param response: 网页response
        :param item: 存储item
        :return:
        """
        item['_id'] = self.snow.get_id()  # 获取雪花算法的id
        item['url'] = response.url  # 网页url
        item['source'] = self.source
        item['sec_title'] = response.meta['sec_title']
        item['insert_date'] = datetime.datetime.now().strftime('%Y-%m-%d')  # 数据插入日期（yyyy-mm-dd）
        item['update_date'] = datetime.datetime.now().strftime('%Y-%m-%d')  # 数据更新日期（yyyy-mm-dd）

    def attach_field(self, response, item):
        """
        附件必填字段
        :param response: 网页response
        :param item: 存储item
        :return:
        """
        item['title'] = response.meta['title']
        item['attachment'] = response.url

    def extract_boxitem(self, info_box, title):
        """
        提取信息盒里面的某一项内容
        [** NOTICE **] 根据自己的网页结构作修改
        北京市信息盒内容格式为：
        <ol>
            <li>
                [主题分类]
                <span>
                综合政务
                </span>
            </li>
            <li>
                [发文日期] 2018-01-02
            </li>
        </ol>
        其中有两种内容格式, 因此要做一定判断
        :param info_box: 信息盒
        :param title: 信息盒里面的title
        :return: 提取内容
        """
        item = info_box.xpath('*//li[contains(string(), "%s")]' % title)
        if not item:
            return None

        span = item.xpath('span')
        if span:
            return span.xpath('text()').extract_first().strip()
        else:
            rep_text = '[%s]' % title
            result = item.xpath('text()').extract_first().replace(rep_text, '').strip()
            if '---' in result:
                return None
            return result

        ## 有些信息盒是信息名称接下来的一个td就是要获取的内容
        ## 这里提供一个实现（不满足条件的不需要return 默认return None）
        # item = info_box.xpath('*//td[contains(string(), "%s")]' % title)
        # if item:
        #     next_td = item.xpath('following-sibling::td[1]/text()').extract_first()
        #     if next_td:
        #         return next_td.strip()
