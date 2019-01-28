# with open('pinyin.py', 'r') as f:
#     file_content = f.readlines()
# print(file_content)

# f = open('pinyin_copy.py', 'w')
# f.writelines(file_content)
import os
import re


def generate(resultdir, rp_quanpin, source):
    """
    项目生成器
    :param resultdir: 结果文件夹
    :param rp_quanpin: 用于替换的项目全拼
    :param source: 来源：贵州省政府
    :return:
    """
    if not os.path.exists(resultdir):
        os.mkdir(resultdir)

    nowdir = os.path.dirname(__file__)
    for root, dirs, files in os.walk(nowdir + '\__BASEPROJ'):
        root_rp = ''
        if '__BASEPROJ' in root:
            root_rp = root.replace(nowdir + '\\', '')
            root_rp = root_rp.replace('__BASEPROJ', rp_quanpin)

        root_mk = '%s\%s' % (resultdir, root_rp)
        if not os.path.exists(root_mk):
            os.mkdir(root_mk)

        # 如果有文件, 按要求创建文件
        if files:
            for file in files:
                file_ori_url = '%s\%s' % (root, file)
                if os.path.splitext(file_ori_url)[-1] == '.pyc':
                    continue
                print('Generate file %s' % file_ori_url)
                # 读取原始文件内容
                with open(file_ori_url, 'r', encoding='utf8') as f_ori:
                    f_ori_lines = f_ori.readlines()
                f_ori.close()

                write_lines = []
                # 替换指定文件内容
                for f_ori_line in f_ori_lines:
                    if '__BASEPROJ' in f_ori_line:
                        f_ori_line = re.sub('__BASEPROJ', rp_quanpin, f_ori_line)
                    if '__SOURCE' in f_ori_line:
                        f_ori_line = re.sub('__SOURCE', source, f_ori_line)

                    write_lines.append(f_ori_line)


                file_dest_url = '%s\%s' % (root_mk, file)
                f_dest = open(file_dest_url, 'w', encoding='utf8')
                f_dest.writelines(write_lines)

