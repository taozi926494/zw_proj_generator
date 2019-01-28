# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base # 用于创建Base基类, ORM对象必须继承Base基类

def create_engine_byconf(DB_CONFIG):
    '''
    自定义一个根据数据库配置创造sqlalchemy engine的函数
    :param DB_CONFIG: MySql数据库配置
    :return: Mysql 数据库引擎
    '''

    # 组装创造sqlalchemy engine的字符串
    # 结果：mysql://root:123456@localhost:3306/ttt?charset=utf8
    engine_words = DB_CONFIG.get('dbtype') + '://' + DB_CONFIG.get('username') + ':' + DB_CONFIG.get('password')\
                   + '@' + DB_CONFIG.get('host') + ':' + DB_CONFIG.get('port') + '/' + DB_CONFIG.get('dbname')\
                   + '?charset=' + DB_CONFIG.get('charset')

    # 调用sqlalchemy的create_engin函数创建一个 sqlalchemy engine
    engine = create_engine(engine_words)
    return engine

def create_session_byengine(engine):
    '''
    根据数据库引擎创建数据库会话session
    :param engine: 数据库引擎
    :return: 数据库会话session
    '''
    Session = sessionmaker(bind=engine)  # 绑定引擎
    session = Session() # 生成session
    return session

def table_existed(ORM_class, db_engine):
    '''
    判断数据库表是否在某个数据库中
    :param table: 要判断ORM类
    :param db_engine: 数据库引擎
    :return: Boolean
    '''
    Base = declarative_base()
    Base.metadata.reflect(db_engine)
    tables = Base.metadata.tables

    if ORM_class.__tablename__ in tables:
        return True
    else:
        return False