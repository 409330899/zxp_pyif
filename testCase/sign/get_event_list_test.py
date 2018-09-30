import unittest
import paramunittest
from common import comm
from common.configLog import MyLog
import readConfig as readConfig
from common import configHttp as configHttp

eventInfo_xls = comm.get_xls("signCase.xlsx", "get_event")
localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
log = MyLog.get_log()
# log.build_log_format()  # 这个格式设置，全runtest只能调用一次，否则将重新输入log的info
logger = log.get_logger()


@paramunittest.parametrized(*eventInfo_xls)
class GetEvent(unittest.TestCase):
    def setParameters(self, case_name, method, eid, name_query, data, name_assert, address, status, msg):
        """
        set params
        :param case_name:
        :param method:
        :param eid:
        :param name_query:
        :param name_assert:
        :param data:
        :param address
        :param status:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.eid = comm.exldataTostr(eid)
        self.name_query = str(name_query)
        self.name_assert = str(name_assert)
        self.address = str(address)
        self.data = comm.exldataTostr(data)
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

    def testGetEvent(self):
        """
        test body
        :return:
        1.参数准备
        2.发送请求
        3.断言
        """
        # set url
        url = comm.get_url_from_xml('event_get')
        localConfigHttp.set_url(url)
        # set params
        if (self.eid == '') and (self.name_query == ''):
            params = None
            print("name和eid为空！")
        elif self.eid != '' and self.name_query == '':
            params = {"eid": self.eid}
            print("params为eid！")
        elif self.eid == '' and self.name_query != '':
            params = {"name": self.name_query}
            print("params为name！")
        elif self.eid != '' and self.name_query != '':
            params = {"eid": self.eid, "name": self.name_query}
            print("name和eid都有值，联合查询！！")
        else:
            print("set params error!")
        localConfigHttp.set_params(params)
        # 发送get请求
        self.response = localConfigHttp.get()
        # 断言结果
        self.checkResult()

    def tearDown(self):
        """
        :return:将测试结果打印输出到log文件中：D:\Python\interfaceTest\result\yyyy-mm-dd\output.log
        """
        logger.info("["+self.case_name+"]" + "Finished!")

    def checkResult(self):
        """打印请求返回的response数据，以及断言（response返回数据VS预期结果）"""
        comm.show_return_msg(self.response)  # 打印response
        self.info = self.response.json()
        # print(self.info)
        if type(self.status) == str:
            status = int(self.status)
        else:
            print("Excel中status状态值检查输入！")
        if self.data == 'no':
            self.assertEqual(self.info["message"], self.msg)
            self.assertEqual(self.info["status"], status)
        else:
            self.assertEqual(self.info["message"], self.msg)
            self.assertEqual(self.info["status"], status)
            name = comm.get_value_from_return_json(self.info, 'data', 'name')
            address = comm.get_value_from_return_json(self.info, 'data', 'address')
            self.assertEqual(name, self.name_assert)
            self.assertEqual(address, self.address)
