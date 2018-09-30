import os
import codecs
import configparser

proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir, "config.ini")


class ReadConfig:
    def __init__(self):
        fd = open(configPath)
        data = fd.read()

        """remove BOM：BOM签名的意思就是告诉编辑器当前文件采用何种编码，方便编辑器识别，
        但是BOM虽然在编辑器中不显示，但是会输出空行。开头的字节流就知道是否是UTF-8编码。
        bom_utf8比utf8多了3个字节前缀"""
        if data[:3] == codecs.BOM_UTF8:  # data[:3]列表数据切片，省略起始位置、步长，结束位置为3
            data = data[3:]  # 从文件的前3个来判断是否为BOM_UTF8，如果是，则从第3个开始取数
            file = codecs.open(configPath, "w")
            file.write(data)  # 如果是BOM编码，则去年前3个字节前缀后，重写文件"config.ini"
            file.close()
        fd.close()

        self.cf = configparser.ConfigParser()  # 实例化读取ini文件的类
        self.cf.read(configPath)

    def get_email(self, name):
        value = self.cf.get("EMAIL", name)  # ini文件读取操作
        return value

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_headers(self, name):
        value = self.cf.get("HEADERS", name)
        return value

    def set_headers(self, name, value):
        self.cf.set("HEADERS", name, value)  # ini文件写入操作

        """由于文件读写都有可能产生IOError，一旦出错，后面的f.close()就不会调用。所以，
        为了保证无论是否出错都能正确关闭文件，可以使用try...finally，也可以使用python
        引入的with语句来自动帮我们调用close()方法"""
        with open(configPath, 'w+') as f:
            self.cf.write(f)

    def get_url(self, name):
        value = self.cf.get("URL", name)
        return value

    def get_db(self, name):
        value = self.cf.get("DATABASE", name)
        return value

    def get_testcasedir(self, name):
        value = self.cf.get("TESTCASEDIR", name)
        return value


if __name__ == "__main__":
    print("proDir:" + proDir)  # 当前目录路径
    print("configPath:" + configPath)  # 当前配置文件路径
    rc = ReadConfig()
    p = rc.get_http("host")
    print(p)
