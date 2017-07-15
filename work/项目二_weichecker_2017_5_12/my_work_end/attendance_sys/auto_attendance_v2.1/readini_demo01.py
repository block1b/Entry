#coding=utf-8
import ConfigParser
import re


# 读取配置文件信息   节次信息    返回一个节次开始和结束时间的列表
class readini():
    List = []
    # List = [['2004633', '51610189', ['\xe8\xbd\xaf\xe4\xbb\xb6\xe5\xb7\xa5\xe7\xa8\x8b1401', '\xe8\xbd\xaf\xe4\xbb\xb6\xe5\xb7\xa5\xe7\xa8\x8b1402', '\xe8\xbd\xaf\xe4\xbb\xb6\xe5\xb7\xa5\xe7\xa8\x8b1403', '\xe8\xae\xa1\xe7\xae\x97\xe6\x9c\xba\xe7\xa7\x91\xe5\xad\xa6\xe4\xb8\x8e\xe6\x8a\x80\xe6\x9c\xaf1401'], '2016-06-09 14:00:21']]

    def __init__(self):

        # self.List = []    #全局队列列表
        pass

    def readIni(self):
        cf = ConfigParser.ConfigParser()
        cf.read('../internal/settings.ini')
        playTimeList = []  # 设置一个列表存两节课的开始和结束时间

        time = re.split('-|:', cf.get('sectime', 'sec1'))
        FirstEndTime = str(time[2]) + str(time[3])
        playTimeList.append(FirstEndTime)
        time = re.split('-|:', cf.get('sectime', 'sec2'))
        SecondStartTime = str(time[0]) + str(time[1])
        playTimeList.append(SecondStartTime)
        # 第三四节课的时间始末
        time = re.split('-|:', cf.get('sectime', 'sec3'))
        ThreeEndtime = str(time[2]) + str(time[3])
        playTimeList.append(ThreeEndtime)
        time = re.split('-|:', cf.get('sectime', 'sec4'))
        FourStartTime = str(time[0]) + str(time[1])
        playTimeList.append(FourStartTime)
        # 第四五节课的时间始末
        FourEndTime = str(time[2]) + str(time[3])
        playTimeList.append(FourEndTime)
        time = re.split('-|:', cf.get('sectime', 'sec5'))
        FiveStartTime = str(time[0]) + str(time[1])
        playTimeList.append(FiveStartTime)

        return playTimeList
if __name__ == "__main__" :
    t = readini()
    print t.List.pop(0)
    print t.List
#     t.List.append("hello")
#     print t.List
    print t.readIni()

