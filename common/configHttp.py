import requests
import sys
import os
import configLog
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
import readConfig

localReadConfig = readConfig.ReadConfig()


class ConfigHttp:
    def __init__(self):
        global scheme, host, port, timeout
        scheme = localReadConfig.get_http("scheme")
        host = localReadConfig.get_http("host")
        port = localReadConfig.get_http("port")
        timeout = localReadConfig.get_http("timeout")
        self.log = configLog.MyLog.get_log()
        self.logger = self.log.get_logger()
        self.headers = {}
        self.params = {}
        self.data = {}
        self.url = None
        self.files = {}
        self.state = 0

    def set_url(self, url):
        """
        set url
        :param: interface url
        :return:
        """
        self.url = scheme+'://'+host+':'+port+'/'+url
        print("请求的URL是:")
        print(self.url)

    def set_headers(self, header):
        """
        set headers
        :param header:
        :return:
        """
        self.headers = header
        print("请求的Headers是:")
        print(self.headers)

    def set_params(self, param):
        """
        set params
        :param param:
        :return:
        """
        self.params = param
        print("请求的params是:")
        print(self.params)

    def set_data(self, data):
        """
        set data
        :param data:
        :return:
        """
        self.data = data
        print("请求的data是:")
        print(self.data)

    def set_files(self, filename):
        """
        set upload files
        :param filename:
        :return:
        """
        if filename != '':
            file_path = 'F:/AppTest/Test/interfaceTest/testFile/img/' + filename
            self.files = {'file': open(file_path, 'rb')}

        if filename == '' or filename is None:
            self.state = 1

    # defined http get method
    def get(self):
        """
        defined get method
        :return:
        """
        try:
            if self.headers == "":
                response = requests.get(self.url, params=self.params)
            else:
                response = requests.get(self.url, headers=self.headers, params=self.params, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    def postData(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, data=self.data)
            return response
        except TimeoutError:
            self.logger.error("Time out!")
        return None

    # defined http post method
    # include get params and post data
    # uninclude upload file
    def post(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, params=self.params, data=self.data, timeout=float(timeout))
            # response.raise_for_status()
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # include upload file
    def postWithFile(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data, files=self.files, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # for json
    def postWithJson(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, json=self.data, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None


if __name__ == "__main__":
    print("ConfigHTTP")
    ch = ConfigHttp()
    ch.set_url('api/get_event_list/')
    ch.set_params({"eid": 1})
    ch.get()


