# coding=utf8
# import threading
# from base_import import BaseImport
#
# def endtime():
#     print "the windows is end"
#
# def hello(s):
#     print "hello, world " + s
#     endtime()
#
# t = threading.Timer(5, hello, ['666'])
# t.start()
# print "Hi after 5 m,will print \"hello, world\""
# t.cancel()
#
# if t.isAlive():
#     print "time is runing \n"

# new_seq_line = [{"TeacherID": None,
#                     "CourseID": None,
#                     "SeqID": "0",
#                     "StartTime": None
#                     }]
#
# b = BaseImport()
# file_name = "../outputdemo/cesi01.csv"
# b.write_file(new_seq_line, file_name)

# filename = "../outputdemo/seq.csv"
# print filename
# path = filename[:-7]
# print path
# import time
# import datetime
# date1 = "2017-05-31 21:19:30"
# date2 = "2017-05-31 21:19:35"
# date1 = time.strptime(date1, "%Y-%m-%d %H:%M:%S")
# date2 = time.strptime(date2, "%Y-%m-%d %H:%M:%S")
# date1 = datetime.datetime(date1[0], date1[1], date1[2], date1[3], date1[4], date1[5])
# date2 = datetime.datetime(date2[0], date2[1], date2[2], date2[3], date2[4], date2[5])
# data3 = (date2-date1).seconds
# print type(data3)
from base_file import BaseFile

b = BaseFile()
date = [{"a": "1", "b": "2"},{"a": "1", "b": "2"},{"a": "1", "b": "2"},{"a": "1", "b": "2"}]
b.write_file(date, "../outputdemo/test01.csv", "ab")
