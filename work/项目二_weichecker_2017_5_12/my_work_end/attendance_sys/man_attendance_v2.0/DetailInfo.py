# coding=utf8
from base_import import BaseImport


class DetailInfo(BaseImport):
    def __init__(self):
        pass

    # detail文件名构建
    def set_detail_filename(self, teacherID, courseID, seqID):
        detail_filename = teacherID + "_" + courseID + "_" + seqID + "_checkinDetail.csv"  # 按要求seqID应为双数，暂时忽略吧。
        return detail_filename

    # 获取detail表信息
    def get_all_detail_info(self, detail_filename):
        all_detail_info = self.read_file(detail_filename)
        return all_detail_info

    # proofpath内容构建 （checkintime中间有空格作为文件名可能有误，注意）
    def set_proofpath(self, stuID, courseID, seqID, checkintime):
        proofpath = "D:/Proof/" + stuID + "_" + courseID + "_" + seqID + "_" + checkintime + ".jpg"
        return proofpath

    # detail表构造行数据
    def set_detail_line(self, stuID, checkintime, proofpath, checkintype, issucc, checkinresult):
        detail_line = {"StuID": stuID,
                       "CheckinTime": checkintime,
                       "ProofPath": proofpath,
                       "CheckinType": checkintype,
                       "IsSucc": issucc,
                       "CheckinResult": checkinresult
                       }
        return detail_line

    # 将新的detail行加入detail表
    def detail_update(self, detail_lines, all_detail_info):
        all_detail_info += detail_lines

        return all_detail_info

    # 将detailed表写入文件
    def write_detail(self, all_detail_info, detail_filename):
        self.write_file(all_detail_info, detail_filename, "wb")
        return

    # 获得detail表的统计结果stu_checkin_result 待定
    def detail_sum(self, all_detail_info):
        DEMOSUMINFO = [
            {"StuID": "201416920128", "CheckinResult": "in"},
            {"StuID": "201416920105", "CheckinResult": "in"}
        ]
        return DEMOSUMINFO