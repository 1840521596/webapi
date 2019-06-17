#!/usr/bin/python
#-*-coding:utf8 -*-
# 定义日志属性，及输出
import logging
import time
class TestLog(object):
    '''
封装后的logging
    '''

    def __init__(self, logger=None):
        '''
            指定保存日志的文件路径，日志级别，以及调用文件
            将日志存入到指定的文件中
        '''

        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        # 创建一个handler，用于写入日志文件
        self.log_time = time.strftime("%Y_%m_%d_")
        #self.log_path = "./app/base/pythonProject/log/"
        self.log_path = "../../log/"
        self.log_name = self.log_path + self.log_time + '_api.log'

        fh = logging.FileHandler(self.log_name, 'a')  # 追加模式  这个是python2的
        fh.setLevel(logging.INFO)

        # 再创建一个handler，用于输出到控制台
        #ch = logging.StreamHandler()
        #ch.setLevel(logging.INFO)

        # 定义handler的输出格式
        formatter = logging.Formatter(
            '[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s]%(message)s')
        fh.setFormatter(formatter)
        #ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        #self.logger.addHandler(ch)

        #  添加下面一句，在记录日志之后移除句柄
        # self.logger.removeHandler(ch)
        # self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()
       # ch.close()

    def getlog(self):
        return self.logger
fengefu = "\n########################################################\n"
lianjiefu = "----*----"