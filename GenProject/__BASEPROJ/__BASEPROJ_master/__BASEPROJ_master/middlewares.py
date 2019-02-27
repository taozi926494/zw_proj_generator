# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import logging
import random
import time

from scrapy import signals
from .utils.user_agents import agents
from scrapy.utils.project import get_project_settings
import requests


class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent

class ProxyMiddleware(object):
    """换代理IP"""
    settings = get_project_settings()
    proxy_list = []
    proxy_expire_time = 0

    def process_request(self, request, spider):
        # 如果是第一次请求
        if not self.proxy_list:
            params = {
                'timestamp': int(time.time()),
                'project': self.settings.get('PROJECT_NAME'),
                'must_list': 1
            }
            response = json.loads(requests.get(url=self.settings.get('PROXY_CENTER_URL'), params=params).text)
            if response['code'] == 200:
                self.proxy_list = response['data']
                self.proxy_expire_time = response['proxy_expire_time']
                logging.info('[Proxy First Get] Success get proxy ip ! Total %s , Expire time %s'
                             % (len(self.proxy_list),
                                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.proxy_expire_time))))
            else:
                self.proxy_list = response['data']
                self.proxy_expire_time = response['proxy_expire_time']
                logging.info('[Proxy First Get] %s ! Total %s , Expire time %s'
                             % (response['msg'], len(self.proxy_list),
                                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.proxy_expire_time))))

        # 如果不是第一次请求
        else:
            # 如果代理IP的过期时间大于当前的时间
            if self.proxy_expire_time > int(time.time()):
                params = {
                    'timestamp': int(time.time()),
                    'project': get_project_settings().get('PROJECT_NAME'),
                }
                response = json.loads(requests.get(url=self.settings.get('PROXY_CENTER_URL'), params=params).text)
                if response['code'] == 200:
                    self.proxy_list = response['data']
                    self.proxy_expire_time = response['proxy_expire_time']
                    logging.info('[Proxy Running Get] Success get proxy ip ! Total %s , Expire time %s'
                                 % (len(self.proxy_list)
                                    , time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.proxy_expire_time))))

        proxy = random.choice(self.proxy_list)
        request.meta['proxy'] = 'http://%s:%s' % (proxy['ip'], proxy['port'])


class GuizhouGongwuyuanjuMasterSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class GuizhouGongwuyuanjuMasterDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
