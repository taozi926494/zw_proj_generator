# -*- coding: utf-8 -*-
# 数据操作相关的函数
# 这里定义的函数与正文内容无关, 所以不会经常改变
# 函数里面有正文内容提取相关的不放在这里定义，直接放到类里面定义
import logging
import os
import re

import scrapy
from scrapy.http import Response
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin

def unify_date(date_str):
    '''
    功能:处理时间为统一格式
    :param data: str 时间字符串
    :return:
    '''
    # 先去掉24小时的时间，例如 11:24:11、11:24
    date_str = re.sub('\s+\d+:\d+:?\d*', '', date_str)
    return date_str.replace(u'年', u'-').replace(u'月', u'-').replace(u'日', u'')

def draftdate_from_textlines(textlines):
    """
    在正文里面去提取成文日期
    :param textlines: 正文的每一行
    :return: 提取结果
    """
    if textlines:
        textlines.reverse()
        for line in textlines:
            line = line.strip()
            is_date = re.search(r'^\d+年\d+月\d+日$', line)
            if is_date:
                return unify_date(is_date.group())

def del_quote(s):
    """
    删除字符串中的中英文冒号
    :param s: str
    :return: str
    """
    return re.sub(':|：', '', s)

def is_attachment(href):
    """
    判断网页链接是否是附件
    :param href: 网页链接
    :return: bool
    """
    # 所有附件的后缀名列表
    attach_postfix = ['.doc', '.docx', '.xls', '.xlsx', '.pdf', '.jpg', '.png', '.jpeg', '.rar', '.txt', '.ceb'
                      '.DOC', '.DOCX', '.XLS', '.XLSX', '.PDF', '.JPG', '.PNG', '.JPEG', '.RAR', '.TXT', '.CEB']
    if os.path.splitext(href)[-1] in attach_postfix:
        return True
    else:
        return False

def unify_url(response, url):
    """
    标准化url路径 （绝对路径和相对路径都会转换成绝对路径）
    :param response: scrapy.Response
    :param url: url
    :return:
    """
    if not isinstance(response, Response):
        logging.error("[** ERROR **] function unify_path(response, url) "
                      "papram response is not instance of scrapy.Response")
    return urljoin(get_base_url(response), url)


def extract_attachments(hrefs, response):
    """
    提取附件
    :param hrefs: 提取出来的超链接列表
    :param response: scrapy.Response
    :return: 返回获取的附件url列表
    """

    # 所有附件的后缀名列表
    attach_postfix = ['.doc', '.docx', '.xls', '.xlsx', '.pdf', '.jpg', '.png', '.jpeg', '.rar', '.txt', '.ceb'
                      '.DOC', '.DOCX', '.XLS', '.XLSX', '.PDF', '.JPG', '.PNG', '.JPEG', '.RAR', '.TXT', '.CEB']
    attach_list = []

    for href in hrefs:
        # 判断获取的超链接的后缀是否为附件格式
        if is_attachment(href):
            unify_url(response, href)
    return attach_list
