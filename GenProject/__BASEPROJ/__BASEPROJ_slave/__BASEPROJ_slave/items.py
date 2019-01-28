# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PaperItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()  # 网页url
    source = scrapy.Field()  # 来源（网站名称（部门机构名称）
    title = scrapy.Field()  # 标题
    text = scrapy.Field()  # 正文
    text_html = scrapy.Field()  # 正文区域源码，为之后解析用
    source_html = scrapy.Field()  # 网页源码

    sec_title = scrapy.Field()  # 章节标题（上表中爬取字段列中链接对应的板块的名称，比如信息
    attachment = scrapy.Field()  # 附件url，可能是列表
    topic = scrapy.Field()  # 主题，导航栏主题信息
    index_number_info = scrapy.Field()  # 索引号
    index_number_info_alias = scrapy.Field()  # 索引号在该网站的原名

    topic_cat_info = scrapy.Field()  # 信息盒的主题分类
    topic_cat_info_alias = scrapy.Field()  # 信息盒的主题分类原名

    pub_office_info = scrapy.Field()  # 信息盒发文机关
    pub_office_info_alias = scrapy.Field()  # 信息盒发文机关原名

    draft_date_info = scrapy.Field()  # 信息盒成文日期
    draft_date_info_alias = scrapy.Field()  # 信息盒成文日期原名

    text_title_info = scrapy.Field()  # 信息盒的标题
    text_title_info_alias = scrapy.Field()  # 信息盒的标题原文

    reference_number_info = scrapy.Field()  # 信息盒的发文字号
    reference_number_info_alias = scrapy.Field()  # 信息盒的发文字号原文

    pub_date_info = scrapy.Field()  # 信息盒的发布日期
    pub_date_info_alias = scrapy.Field()  # 信息盒的发布日期原文

    topic_words_info = scrapy.Field()  # 信息盒的主题词
    topic_words_info_alias = scrapy.Field()  # 信息盒主题词原文

    source_info = scrapy.Field()  # 信息盒的信息来源
    source_info_alias = scrapy.Field()  # 信息盒信息来源原名

    summary_info = scrapy.Field()  # 信息盒的内容概述
    summary_info_alias = scrapy.Field()  # 信息盒的内容概述原名

    form_code_info = scrapy.Field()  # 信息盒的形式代码
    form_code_info_alias = scrapy.Field()  # 信息盒的形式代码原名

    theme_info = scrapy.Field()  # 信息盒的体裁
    theme_info_alias = scrapy.Field()  # 信息盒的体裁原名

    effective_date_info = scrapy.Field()  # 信息盒的生效日期
    effective_date_info_alias = scrapy.Field()  # 信息盒的生效日期原名

    expire_date_info = scrapy.Field()  # 信息盒的失效日期
    expire_date_info_alias = scrapy.Field()  # 信息盒的失效日期原名

    insert_date = scrapy.Field()  # 数据插入日期（yyyy-mm-dd）
    update_date = scrapy.Field()  # 更新日期（yyyy-mm-dd）
