'''
北京市政府文件分为近三年内的政策文件和三年以上的政策文件
且两者的列表页和详情页提取方式不同
因此以sign：new、old做标记
'''

catelogs = [
    {
        "url": "http://www.beijing.gov.cn/zhengce/zfwj/5111/5121/1344471/index.html",
        "extract_rule": "xpath",
        "extract_code": "//ul[@class='list']/li",
        "sec_title": "政府文件",
        "sign": "new"
    },
    # {
    #     "url": "http://www.beijing.gov.cn/zhengce/zfwj/25/26/421256/index.html",
    #     "extract_rule": "xpath",
    #     "extract_code": "",
    #     "sec_title": "政府文件",
    #     "sign": "new"
    # }
    # 市政府办公厅文件

]