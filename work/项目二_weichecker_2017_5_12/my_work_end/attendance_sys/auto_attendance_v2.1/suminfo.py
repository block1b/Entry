# coding=utf8
from base_file import BaseFile


class SumInfo(BaseFile):
    def __init__(self):
        pass

    # sum 文件名构建
    def set_sum_filename(self, teacherID, courseID):
        sum_filename = teacherID + "_" + courseID + "_sum.csv"
        return sum_filename

    # 获取sum表数据
    def get_all_sum_info(self, sum_filename):
        all_sum_info = self.read_file(sum_filename)
        return all_sum_info

    # CheckinID构建
    def set_checkinseqid(self, seqID):
        """
        构建sum中的新表头
        :param seqID: 
        :return: 
        """
        checkinseqid = "Checkin" + seqID
        return checkinseqid

    # sum表行数据更新
    def sum_line_update(self, sum_line, checkinseqid, checkinresult):
        sum_line.update({checkinseqid: checkinresult})
        return sum_line

    # 更新sum表数据
    def sum_update(self, stu_checkin_result, sum_info, checkinseqid):
        for internal_sun_line in sum_info:
            for demo_sum_line in stu_checkin_result:
                if internal_sun_line["StuID"] == demo_sum_line["StuID"]:
                    self.sum_line_update(internal_sun_line, checkinseqid,
                                        demo_sum_line[checkinseqid])
        return sum_info

    # sum表初始化
    def sum_creat(self, stuids):
        """
        初始化sum表
        :param stuids: 
        :return: 
        """
        sum_data = []
        for stuid in stuids:
            sum_data.append({"StuID": stuid})
        return sum_data

    # 将sum表写入文件
    def write_sum(self, sum_data, sum_filename):
        self.write_file(sum_data, sum_filename, "wb")
        return

if __name__ == "__main__":
    # 请假批准
    s = SumInfo()
    SUMFILENAME = "../outputdemo/2004643_51610145_1_checkinDetail.csv"
    all_detail_info = s.get_all_sum_info(SUMFILENAME)
    print all_detail_info
    for detail_line in all_detail_info:
        print detail_line
        if detail_line["CheckinResult"] == "zt":
            print detail_line["ProofPath"]
            detail_line["CheckinResult"] = "qj"
            print detail_line