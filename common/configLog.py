import os
import readConfig as readConfig
import logging
from datetime import datetime
import threading
import time

localReadConfig = readConfig.ReadConfig()


class LogMain:
    def __init__(self):
        """使用global清楚地表明变量在外面的块定义的。只能定义，不能定义的同时赋值。"""
        global logPath, resultPath, proDir
        proDir = readConfig.proDir
        resultPath = os.path.join(proDir, "result")
        if not os.path.exists(resultPath):
            os.mkdir(resultPath)
        logPath = os.path.join(resultPath, str(datetime.now().strftime("%Y%m%d%H%M%S")))
        if not os.path.exists(logPath):
            os.mkdir(logPath)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    def build_log_format(self):
        # defined handler
        handler = logging.FileHandler(os.path.join(logPath, "output.log"))
        # defined formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_logger(self):
        """
        get logger
        :return:
        此方法方便定义日志级别，如logger.info,logger.error
        如：configHttp中定义日志级别
        """
        return self.logger

    def build_line(self, something):
        """
        write end line
        :return:
        """
        self.logger.info(something)

    def build_start_line(self, something):
        """
        write start line
        :return:
        """
        self.logger.info("---"+something+"---")

    def build_end_line(self, something):
        """
        write end line
        :return:
        """
        self.logger.info("---"+something+"---")

    def build_case_line(self, case_name, code, msg):
        """
        write test case line
        :param case_name:
        :param code:
        :param msg:
        :return:
        """
        self.logger.info("用例名称:"+case_name+" - 执行状态:"+code+" - 回送消息:"+msg)

    def get_report_path(self):
        """
        get report file path
        :return:html报告路径
        """
        now = time.strftime("%Y-%m-%d %H_%M_%S")
        report_path = logPath + '\\' + '测试结果报告' + now + '.html'
        return report_path

    def get_result_path(self):
        """
        get test result path
        :return:
        log日志路径
        """
        return logPath

    def write_result(self, result):
        """
        :param result:
        :return:
        写入日志
        """
        result_path = os.path.join(logPath, "report.txt")
        fb = open(result_path, "wb")
        try:
            fb.write(result)
        except FileNotFoundError as ex:
            self.logger.error(str(ex))


class MyLog:
    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_log():

        if MyLog.log is None:
            MyLog.mutex.acquire()
            MyLog.log = LogMain()
            MyLog.mutex.release()

        return MyLog.log


if __name__ == "__main__":
    log = MyLog.get_log()
    log.build_log_format()
    log.build_start_line("info")
    print(log.get_report_path())
    print(log.get_result_path())
    # logger = log.get_logger()
    # logger.debug("test debug")
    # logger.info("test info")

    # log = MyLog.get_log()
    # log.logger_format()
    # logger = log.get_logger()
    # log.build_start_line("START:")
    # log.build_end_line("END!")
    # log.build_end_line("**************************************")

