import os
import sys

if __name__ == '__main__':
    BASE_DIR = os.path.dirname(__file__)
    sys.path.append(BASE_DIR)
    from GenProject import gen

    # 城市名，规范：带省、市、自治区
    # 例如：北京市 | 贵州省 | 西藏自治区
    city = '贵州省'

    # 部门名称
    section = '公务员局'

    gen(r"D:\Code\Python\crawlers\zhiwen-知文智用\guizhou-贵州省公文公告\xht谢红韬\new", city, section, repl_postfix=True)