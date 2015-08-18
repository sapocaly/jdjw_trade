__author__ = 'Sapocaly'

import threading

#1.初始化一个fetcher生命周期内所有需要准备的
#2.准备单次fetch的数据
#3.并行及线性fetch,check数据,check方法被包裹处理并行问题
#4.尝试n次插入
#5.失败报错,成功保存,清理数据


class Fetcher(object):

    def __init__(self):
        pass

    def initialize(self):
        pass

    def prepare(self):
        self.success = False
        pass

    def fetch(self):
        pass

    def parallel_try(self):

        pass

    def linear_try(self):
        pass

    def check(self):
        pass

    def save(self):
        pass

    def fetch(self):
        self.prepare()
        self.linear_try()


def parallel_wrapper():
    pass