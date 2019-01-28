import re

from .generator import generate
from .pinyin import gen_quanpin


def gen(result_dir, city_cn, section_cn, repl_postfix=True):
    """
    生成项目
    :param result_dir: 项目生成后存放地址
    :param city_cn: 城市中文名
    :param section_cn: 部门中文名
    :param repl_postfix: bool 是否替换掉县、市、自治区（默认True,可选False 如：沛县: 不替换）
    :return:
    """
    source = city_cn + section_cn
    if repl_postfix:
        city_cn = re.sub('县|市|自治区', '', city_cn)
    city_qp = gen_quanpin(city_cn)  # 城市全拼
    section_qp = gen_quanpin(section_cn)  # 部门全拼
    project_qp = '%s_%s' % (city_qp, section_qp)

    generate(result_dir, project_qp, source)
