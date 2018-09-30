import unittest
import requests
import time
import datetime
import sys
import os
import unittest
import paramunittest
from common import comm
from common.configLog import MyLog
import readConfig as readConfig
from common import configHttp as configHttp
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)

eventInfo_xls = comm.get_xls("signCase.xlsx", "user_sign")  # 1.修改Excel读取文件！
localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
log = MyLog.get_log()
# log.build_log_format()  # 这个格式设置，全runtest只能调用一次，否则将重新输入log的info
logger = log.get_logger()


@paramunittest.parametrized(*eventInfo_xls)
class AddGuest(unittest.TestCase):
    def setParameters(self, case_name, method, eid, phone, status, msg):
        """
        set params
        :param case_name:
        :param method:
        :param eid:
        :param phone:
        :param status:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.eid = comm.exldataTostr(eid)
        self.phone = comm.exldataTostr(phone)
        self.status = comm.exldataTostr(status)
        self.msg = str(msg)
        self.response = None
        self.info = None

    def description(self):
        """
        :return:返回Excel中的case_name
        """
        self.case_name

    def setUp(self):
        """
        :return:
        """
        logger.info("[" + self.case_name + "]" + "Start:")

    def testAddGuest(self):
        """
        test body
        :return:
        1.参数准备
        2.发送请求
        3.断言
        """
        # set url
        self.url = comm.get_url_from_xml('user_sign')  # 2.修改URL读取文件
        localConfigHttp.set_url(self.url)
        # set data
        data = {'eid': self.eid, 'phone': self.phone}
        localConfigHttp.set_data(data)
        # 发送get请求
        if self.method == 'post':
            self.response = localConfigHttp.postData()
        else:
            print("请确认是请求方式：POST or GET？")
        # 断言结果
        self.checkResult()

    def tearDown(self):
        """
        :return:将测试结果打印输出到log文件中：D:\Python\interfaceTest\result\yyyy-mm-dd\output.log
        """
        # log.build_case_line(self.case_name, str(self.info['status']), self.info['message'])
        # log.build_end_line(self.case_name + "END!")
        logger.info("["+self.case_name+"]" + "Finished!")

    def checkResult(self):
        """打印请求返回的response数据，以及断言（response返回数据VS预期结果）"""
        comm.show_return_msg(self.response)  # 打印返回的jason
        self.info = self.response.json()
        if type(self.status) == str:
            status = int(self.status)
        else:
            print("Excel中status状态值检查输入！")
        self.assertEqual(self.info["message"], self.msg)
        self.assertEqual(self.info["status"], status)
