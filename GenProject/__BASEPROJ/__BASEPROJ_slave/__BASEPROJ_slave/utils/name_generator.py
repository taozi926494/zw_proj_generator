'''
生成组合名称的模块
用于从settings.py中提取工程名称来生成相对应的爬虫名，数据库名等等组合名称
'''

from scrapy.utils.project import get_project_settings

def gen_name(add_name=''):
    '''
    功能：生成组合名称
    从setting.py中获取工程名，并在后面加上 自定义后缀标识 作为生成名
    :param add_name: str 组合名称名称的后缀
    :return: str 组合名称
    '''
    settings = get_project_settings()
    project_name = settings.get('PROJECT_NAME', None)
    if project_name:
        name = project_name + add_name
        return name
    else:
        raise ValueError('Cannot get setting value PROJECT_NAME ! 获取不到settings.py文件中的PROJECT_NAME值')

def spidername_master():
    '''
    生成主爬虫名称
    :return: str 主爬虫名
    '''
    return gen_name('_master')

def spidername_slave():
    '''
    生成从爬虫名称
    :return: str 从爬虫名
    '''
    return gen_name('_slave')

def redis_collection():
    '''
    生成redis collection名
    :return: str redis collection名
    '''
    return gen_name(':start_urls')

def mongo_tablename():
    '''
    生成mongodb的表名
    :return: str mongodb表名
    '''
    return gen_name()