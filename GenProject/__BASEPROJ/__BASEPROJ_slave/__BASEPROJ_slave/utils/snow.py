#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import socket


class Snow:
    """
     目的: pymongo的_id中是数字与字母的组合, 不方便进行排序, 所以使用雪花算法, 生成全数字的_id
     功能： 生成17位的_id, 格式：10时间戳+3为机器标示id+5位同秒级自增id
     使用方法:
        1). item 中添加_id字段
        2). 在spider内实例化 snow = Snow(machine_id)  # machine_id为str, 如"180", 表示172.10.10.180的机器
        3). 在最后返回数据时, item['id'] = snow.get_id()
    """
    # 获取本机的主机名
    hostname = socket.gethostname()
    # 获取本机的IP
    ip = socket.gethostbyname(hostname)
    def __init__(self):
        # 当前时间
        self.last = int(time.time())
        # 计数id
        self.countID = 0
        # 机器标识ID，这个自定义或是映射
        self.dataID = self.ip.split('.')[-1]

    def get_id(self):
        # 当前时间戳
        now = int(time.time())
        if now == self.last:
            self.countID += 1
        # 不同时间差，序列号重新置为0
        else:
            self.countID = 0
            self.last = now
        # 判断dataID的长短是否小于3, 不足3位前面补0
        if len(str(self.dataID)) < 3:
            length = len(str(self.dataID))
            s = "0" * (3-length)
            self.dataID = s + str(self.dataID)
        # 如果序列号自增5位满了，睡眠一秒钟
        if self.countID == 99999:
            time.sleep(1)
        # 转为str
        countIDdata = str(self.countID)
        # 如果序列号不够5位的在前面补0
        if len(countIDdata) < 5:
            length = len(countIDdata)
            s = "0"*(5-length)
            countIDdata = s + countIDdata
        id = str(now) + str(self.dataID) + countIDdata
        return id



