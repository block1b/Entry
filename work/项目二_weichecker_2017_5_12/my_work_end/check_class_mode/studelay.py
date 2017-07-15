# encoding=utf-8

from stucommonmethod import stuMethod
import csv
import time

class stuDelay(stuMethod):

    #对学生请假类的初始化
    def __init__(self):
        stuMethod.__init__(self)
        pass


    #学生进行请假
    def stuLeave(self,_stuWechatID,inputStream):
        stuID = self.checkStudent(_stuWechatID)[0]
        fileName = self.checkFileName(_stuWechatID)
        checkinTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        ProofPath = inputStream
        checkinType = 'Auto'
        IsSucc = ''
        checkinResult = '请假'

        if fileName=='':
            print '打开详细表失败，或许是考勤窗口已经关闭'
            return
        else:
            with open(fileName, 'a') as checkfile:
                writer = csv.writer(checkfile)
                message0 = [stuID, checkinTime, ProofPath, checkinType, IsSucc, checkinResult]
                writer.writerow(message0)
                print '你已进行了请假的操作'
