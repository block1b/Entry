# coding=utf8
import random
# 参数：列表["a", "b", "c", "d", "e"]

arry = ["a", "b", "c", "d", "e"]
print arry
alice = random.sample(arry, 3)
print alice

a = []
a.append("1")
a.append("2")

b = {"name": "汉堡包"}


def showWhat():
    pass

import time
'''
这是多行注释
'''


class Base(object):
    def list(self):
        """
        这是方法说明
        :return:
        """
        pass

    def cag(self):  # this is wrong
        pass

    # 构造一条seq记录
    def set_seq_line(self, teacherID, courseID, seqID, startTime):
        pass
