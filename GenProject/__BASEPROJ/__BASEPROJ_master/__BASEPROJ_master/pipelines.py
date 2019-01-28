# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from pymongo import MongoClient
import redis
from .utils import name_generator

class PaperListItemPipeline(object):

    def __init__(self, mongo_host, mongo_port, mongo_dbname, redis_host, redis_port):
        self.data_count = 0  # 获取数量统计
        # 定义存储爬取数据的数据库的参数
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_dbname = mongo_dbname

        self.redis_host = redis_host
        self.redis_port = redis_port

        self.mongo_tablename = name_generator.mongo_tablename()  # mongodb的数据库名与工程名相同
        self.redis_collection = name_generator.redis_collection()  # redis的数据库名为工程名 + :start_urls

    @classmethod
    def from_crawler(cls, crawler):
        """
        功能: scrapy为我们访问settings提供了这样的一个方法，这里，
        我们需要从需要从settings.py文件中，文件中，取得数据库的URI和数据库名称
        """
        # mongodb的配置
        MONGO_HOST = crawler.settings.get('MONGO_HOST', None)
        MONGO_PORT = crawler.settings.get('MONGO_PORT', None)
        MONGO_DBNAME = crawler.settings.get('MONGO_DBNAME', None)
        # redis的配置
        REDIS_HOST = crawler.settings.get('REDIS_HOST', None)
        REDIS_PORT = crawler.settings.get('REDIS_PORT', None)

        if all([MONGO_HOST, MONGO_PORT, MONGO_DBNAME, REDIS_HOST, REDIS_PORT]):
            return cls(mongo_host=MONGO_HOST, mongo_port=MONGO_PORT, mongo_dbname=MONGO_DBNAME,
                       redis_host=REDIS_HOST, redis_port=REDIS_PORT)
        else:
            raise ValueError('No config MongoDB and Redis connection setting !'
                             ' settings.py 中 MongoDB及Redis 的连接信息未正确配置')

    def open_spider(self, spider):
        """
        爬虫一旦开启，就会实现这个方法，连接到数据库
        :param spider:
        :return:
        """
        try:
            self.mongo_client = MongoClient(self.mongo_host, self.mongo_port)
            self.mongo_dbsession = self.mongo_client[self.mongo_dbname]
        except ConnectionError:
            raise ConnectionError('Cannot connect MongoDB ! 无法连接MongoDB')

        try:
            self.rediscli = redis.Redis(host=self.redis_host, port=self.redis_port, db=0)
        except ConnectionError:
            raise ConnectionError('Cannot connect Redis ! 无法连接Redis')

    def close_spider(self, spider):
        """
        爬虫一旦关闭，就会实现这个方法，关闭数据库连接
        :param spider:
        :return:
        """
        self.mongo_client.close()


    def process_item(self, item, spider):
        """
        处理从列表页提取的详情页url Pipeline，找出在数据库里面不存在的，放进redis列表
        :param item: item对象
        :param spider: spider对象
        :return: item
        """
        paper_list = item['paper_list']
        paper_urls = [paper['url'] for paper in paper_list]
        table = self.mongo_dbsession[self.mongo_tablename]
        # 找出从页码提取的详情页url中，哪些是数据库里面已经存在的，即：爬取过后的url
        crawled_indb = table.find({"url": {"$in": paper_urls}},
                                  {"url": 1})

        for crawled in crawled_indb:
            for paper in paper_list:
                if paper['url'] == crawled['url']:
                    paper_list.remove(paper)
                    break

        # 数据库里面没有从页码提取的详情页url，则push到redis
        if paper_list:
            for paper in paper_list:
                self.rediscli.lpush(self.redis_collection, json.dumps(paper))
