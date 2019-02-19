# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

from pymongo import MongoClient
from .Db.DbInfo import DB_CONFIG_INCRE_COUNT, SpiderIncreCount
from .Db.SqlHandler import create_session_byengine, create_engine_byconf
import socket
import time
from .utils import name_generator

class PaperItemPipeline(object):
    def __init__(self, mongo_host, mongo_port, mongo_dbname):
        self.data_count = 0  # 获取数量统计
        # 定义存储爬取数据的数据库的参数
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_dbname = mongo_dbname
        self.mongo_tablename = name_generator.mongo_tablename()  # mongodb的数据库名与工程名相同

        # 获取本机ip
        hostname = socket.gethostname()
        self.ip = socket.gethostbyname(hostname)

    def gen_timestamp(self, day=0, hour=0, minute=0, second=0):
        '''
        生成当前时间的时间戳
        :return: datetime '2018-09-16 12:21:15'
        '''
        timestamp = time.time() + day * 86400 + hour * 3600 + minute * 60 + second
        nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
        return nowtime

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

        if all([MONGO_HOST, MONGO_PORT, MONGO_DBNAME]):
            return cls(mongo_host=MONGO_HOST, mongo_port=MONGO_PORT, mongo_dbname=MONGO_DBNAME)
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

    def close_spider(self, spider):
        """
        爬虫一旦关闭，就会实现这个方法，关闭数据库连接
        :param spider:
        :return:
        """
        self.mongo_client.close()

        # Sqlalchemy引擎--统计本次爬虫的运行获取了多少条数据的数据库
        incre_count_engine = create_engine_byconf(DB_CONFIG_INCRE_COUNT)
        # Sqlalchemy session--统计本次爬虫的运行获取了多少条数据的数据库
        incre_count_session = create_session_byengine(incre_count_engine)

        project_name = name_generator.gen_name()  # 工程名 **必须与上传到爬虫平台的英文工程名同名
        spider_name = name_generator.spidername_master()  # 爬虫名

        crawl_time = self.gen_timestamp()  # 爬虫关闭的时间

        db_type = 'mongodb'  # 用于存储爬取数据 的数据库类型
        db_ip = '{host}:{port}'.format(host=self.mongo_host, port=self.mongo_port)  # 用于存储爬取数据 的数据库ip(含端口)
        db_name = self.mongo_dbname  # 用于存储爬取数据 的数据库名称
        table_name = self.mongo_tablename  # 用于存储爬取数据 的数据表

        # 向统计本次爬虫的运行获取了多少条数据的数据库 插入统计的数据
        try:
            incre_count_session.add(SpiderIncreCount(project_name=project_name, spider_name=spider_name
                                                     , crawl_time=crawl_time, db_type=db_type,
                                                     db_ip=db_ip
                                                     , db_name=db_name, table_name=table_name,
                                                     data_count=self.data_count, machine_ip=self.ip))
            incre_count_session.commit()
        except Exception as err:
            logging.error('ERROR when insert Increment Data Table')
            print(repr(err))
        incre_count_session.close()

    def process_item(self, item, spider):
        """
        功能: 数据清洗并保存每个实现保存的类里面必须都要有这个方法,且名字固定, 用来具体实现怎么保存
        :param item: item对象
        :param spider: spider对象
        :return: item
        """
        data = {}
        # 遍历item, 将没有值的字段删除
        for k, v in item.items():
            if v:
                data[k] = v
        table = self.mongo_dbsession[self.mongo_tablename]
        table.insert_one(data)
        # 每次成功爬取并存储一个数据, 数据统计量+1
        self.data_count = self.data_count + 1
