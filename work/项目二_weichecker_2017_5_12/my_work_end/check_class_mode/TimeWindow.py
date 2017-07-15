#-*- coding=utf-8 -*-
import threading
from __init__ import readini


class Timer():

    def __init__(self):
        self.t = None

    # 独立的踢出队列函数
    def timeCheck(self):
        if readini.List == []:
            print "the queue is empty!"
            return
        else:
            readini.List.pop(0)
            self.stopCheckIn()

    # 教师进入队列后开始进行倒计时   只在第一个教师进入队列时调用
    def startCheckTime(self):
            self.t = threading.Timer(30, self.timeCheck)
            self.t.start()

    '''教师被踢出队列时需要重新计时,或者自动到时间后教师被提出队列，
        此处只计算与下一位的差值，并重新计时
    '''
    def stopCheckIn(self):
        if self.t != None:
            if readini.List != [] :
                r = readini()
                clist = r.readIni()
                leaveTime = clist[0][3]
                leaveTimeArray = leaveTime.split('-| | :')

                beginTime = clist[1][3]
                beginTimeArray = beginTime.split('-| | :')

                #获得时间的差值 并将其赋给计时器
                timedev = (int(beginTimeArray[3]) - int(leaveTimeArray[3])) * 3600 + (int(beginTimeArray[4]) - int(leaveTimeArray[4])) * 60 + \
                        (int(beginTimeArray[5]) - int(leaveTimeArray[5]))
                readini.List.pop(0)  # 计算后将教师踢出队列
                # 先取消上次计时后，再传入新的计时值
                self.t.cancel()
                self.t = threading.Timer(timedev, self.timeCheck)
                self.t.start()
            else:
                print '当前队列已经没有教师'
                return
        else:
            self.t = threading.Timer(10,self.timeCheck)
            self.t.start()


if __name__ == '__main__':
    t = Timer()
    t.stopCheckIn()








'''
当前实现方法：
    在第一个教师进入队列时，开启一个线程开始倒计时，时间是45×2+10分钟。
    假设：之间没有错误。就是第一个大时间内没问题，直到时间结束，队首的教师被提出队列，此时计时器被销毁，开始下一个计时器
    即：队首的教师和第二个教师的时间差值，重置一个计时器。之后，重复此类操作。
'''


'''
之前思路：
    在教师进入队列时，开启一个线程，对当前的时间开始以默认的时间进行倒计时，到达终点时将队列首的教师踢出队列。
    如果中间有教师被提出队列时，需要重新将倒计时进行重置，（在测试中发现当前的线程数量始终是1？为什么？）
    :搜到说是python中有一个全局解释锁（GIL）

    如果不重置此倒计时，就会出现多个线程到达终点时将教师踢出，那么就会出现队首的教师被提出去好多个（就是线程被开启的个数，怎么解决？）
'''