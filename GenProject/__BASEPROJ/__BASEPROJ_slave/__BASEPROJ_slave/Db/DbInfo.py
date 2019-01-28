# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Enum, Date, DateTime, Text, Numeric, Boolean, SmallInteger, DECIMAL, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base # 用于创建Base基类, ORM对象必须继承Base基类

# # 自定义数据库配置
# DB_CONFIG = {
#     'dbtype': 'mysql',
#     'host': '172.10.10.204',
#     'dbname': '__BASEPROJ',
#     'username': 'root',
#     'password': 'root',
#     'port': '3306',
#     'charset': 'utf8'
# }

'''
统计本次爬虫的运行获取了多少条数据
的数据库配置
'''
DB_CONFIG_INCRE_COUNT = {
    'dbtype': 'mysql',
    'host': '172.10.10.204',
    'dbname': 'SPIDER_INCRE_COUNT',
    'username': 'root',
    'password': 'root',
    'port': '3306',
    'charset': 'utf8'
}

Base = declarative_base() # 创建Base基类, ORM对象必须继承Base基类

'''
统计本次爬虫的运行获取了多少条数据
的数据库表ORM类
'''
class SpiderIncreCount(Base):
    __tablename__ = 'DATA_COUNT'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    project_name = Column(String(255))  # 工程名 **必须与上传到爬虫平台的英文工程名同名
    spider_name = Column(String(255))  # 爬虫名
    crawl_time = Column(DateTime)  # 爬虫关闭的时间
    data_count = Column(Integer)  # 统计的爬取了多少数据
    db_type = Column(String(255))  # 用于存储爬取数据 的数据库类型
    db_ip = Column(String(255))  # 用于存储爬取数据 的数据库ip
    db_name = Column(String(255))  # 用于存储爬取数据 的数据库名称
    table_name = Column(String(255))  # 用于存储爬取数据 的数据表
    data_size = Column(DECIMAL(15, 3))  # 如果爬取的结果是文件类型 统计爬取文件的大小
    machine_ip = Column(String(255))  # 调度该爬虫的机器ip


