# encoding=utf-8

# This program show the student's operations

from stucommonmethod import stuMethod
import csv
import time
import random

class stuCheckIn(stuMethod):

    #对学生正常考勤类进行初始化
    def __init__(self):
        stuMethod.__init__(self)
        pass

    #学生进行正常的自主考勤
    def stuAutoCheckIn(self,_stuWechatID,inputStream):
        stuID = self.checkStudent(_stuWechatID)[0]
        fileName = self.checkFileName(_stuWechatID)
        checkinTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        ProofPath = inputStream
        checkinType = 'Auto'
        IsSucc = bool(random.randrange(0, 2))
        checkinResult = None

        if fileName=='':
            print '打开详细表失败，或许是考勤窗口已经关闭'
            return
        else:
            with open(fileName, 'a+') as checkfile:
                writer = csv.writer(checkfile)
                message0 = [stuID, checkinTime, ProofPath, checkinType, IsSucc, checkinResult]
                writer.writerow(message0)
                print '你已进行了正常考勤的操作'


