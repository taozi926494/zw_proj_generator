import pypinyin

def gen_quanpin(chn):
    return ''.join(pypinyin.lazy_pinyin(chn))