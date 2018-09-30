import os
import unittest
from common.configLog import MyLog
import readConfig as readConfig
import HTMLTestRunner
import common.comm as comm
from common.configEmail import MyEmail
from common import configTData

localReadConfig = readConfig.ReadConfig()
log = MyLog.get_log()
log.build_log_format()  # 这个定义格式的整个测试，只能调用一次，否则将重复打印log的info
logger = log.get_logger()


class AllTest:
    def __init__(self):
        self.reportpath = log.get_report_path()
        testcasedir = localReadConfig.get_testcasedir("dir")
        self.caseListFile = os.path.join(readConfig.proDir, "caselist.txt")
        self.caseFile = os.path.join(readConfig.proDir, "testCase") + '\\' + testcasedir
        self.caseList = comm.get_testcase_from_txt()
        self.email = MyEmail.get_email()

    def set_case_suite(self):
        """
        set case suite
        :return:
        """
        test_suite = unittest.TestSuite()
        suite_module = []

        for case in self.caseList:
            case_name = case.split("/")[-1]
            # print(case_name+".py")
            # print(self.caseFile)
            # print(case_name)
            # 指定执行的目录
            discover = unittest.defaultTestLoader.discover(self.caseFile,
                                                           pattern=case_name + '.py',
                                                           top_level_dir=None)
            suite_module.append(discover)
            # print(suite_module)

        if len(suite_module) > 0:
            for suite in suite_module:
                # print(suite)
                for test_name in suite:
                    test_suite.addTest(test_name)
                    # print(test_name)
        else:
            return None

        return test_suite

    def run(self):
        """
        run test
        :return:
        """
        try:
            suit = self.set_case_suite()
            # print(suit)
            if suit is not None:
                logger.info("********All TEST START********")
                fp = open(self.reportpath, 'wb')
                runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                                       title='Test Report',
                                                       description='如下，是详细测试报告，请查阅')
                configTData.init_data()  # 在执行测试之后，初始化数据库数据为测试数据。
                runner.run(suit)
            else:
                # logger.info("Have no case to test.")
                print("没有要执行的用例！")
        except Exception as ex:
            # logger.error(str(ex))
            print(str.ex)
        finally:
            logger.info("*********All TEST END*********")
            fp.close()


if __name__ == '__main__':
    obj = AllTest()
    obj.run()
