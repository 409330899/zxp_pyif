import requests
import os
import sys
from xlrd import open_workbook
from xml.etree import ElementTree as ElementTree
from common import configHttp as configHttp
from configLog import MyLog
import json
import readConfig

localReadConfig = readConfig.ReadConfig()
proDir = readConfig.proDir
localConfigHttp = configHttp.ConfigHttp()
log = MyLog.get_log()
logger = log.get_logger()

caseNo = 0


def get_visitor_token():
    """
    create a token for visitor
    :return:
    """
    host = localReadConfig.get_http("BASEURL")
    response = requests.get(host+"/v2/User/Token/generate")
    info = response.json()
    token = info.get("info")
    logger.debug("Create token:%s" % (token))
    return token


def set_visitor_token_to_config():
    """
    set token that created for visitor to config
    :return:
    """
    token_v = get_visitor_token()
    localReadConfig.set_headers("TOKEN_V", token_v)


def get_value_from_return_json(json, name1, name2):
    """
    get value by key
    :param json:
    :param name1:
    :param name2:
    :return:
    """
    """从多层jason:{info:{'a': {'b': 'bbb'}}}中取value"""
    info = json[name1]
    if type(info) == dict:
        # print(info)
        value = info[name2]
        # print(value)
        # value = group[name2]
    elif type(info) == list:
        value = info[0][name2]
    return value


def show_return_msg(response):
    """
    show msg detail
    :param response:
    :return:
    """
    url = response.url
    msg = response.text
    print("Response地址："+url+'\n')
    # print("Response地址返回值："+'\n'+json.dumps(json.loads(msg), ensure_ascii=False, sort_keys=True, indent=4)+'\n')


# ****************************** read testCase excel ********************************
# 从excel文件中读取测试用例
def get_xls(xls_name, sheet_name):
    """
    get interface data from xls file
    :return:
    """
    cls = []
    # get xls file's path
    xlsPath = os.path.join(proDir, "testFile", 'case', xls_name)
    # open xls file
    file = open_workbook(xlsPath)
    # get sheet by name
    sheet = file.sheet_by_name(sheet_name)
    # get one sheet's rows
    nrows = sheet.nrows
    for i in range(nrows):
        if sheet.row_values(i)[0] != u'case_name':
            cls.append(sheet.row_values(i))
    return cls

# ****************************** read SQL xml ********************************
database = {}


# 从xml文件中读取sql语句
def set_xml():
    """
    set sql xml
    :return:
    """
    if len(database) == 0:
        sql_path = os.path.join(proDir, "testFile", "SQL.xml")
        tree = ElementTree.parse(sql_path)
        for db in tree.findall("database"):
            db_name = db.get("name")
            # print(db_name)
            table = {}
            for tb in db.getchildren():
                table_name = tb.get("name")
                # print(table_name)
                sql = {}
                for data in tb.getchildren():
                    sql_id = data.get("id")
                    # print(sql_id)
                    sql[sql_id] = data.text
                table[table_name] = sql
            database[db_name] = table


def get_xml_dict(database_name, table_name):
    """
    get db dict by given name
    :param database_name:
    :param table_name:
    :return:
    """
    set_xml()
    database_dict = database.get(database_name).get(table_name)
    return database_dict


def get_sql(database_name, table_name, sql_id):
    """
    get sql by given name and sql_id
    :param database_name:
    :param table_name:
    :param sql_id:
    :return:
    """
    db = get_xml_dict(database_name, table_name)
    sql = db.get(sql_id)
    return sql
# ****************************** read interfaceURL xml ********************************


def get_url_from_xml(name):
    """
    By name get url from interfaceURL.xml
    :param name: interface's url name
    :return: url
    """
    url_list = []
    url_path = os.path.join(proDir, 'testFile', 'interfaceURL.xml')
    tree = ElementTree.parse(url_path)
    for u in tree.findall('url'):
        url_name = u.get('name')
        if url_name == name:
            for c in u.getchildren():
                url_list.append(c.text)
    url = '/'.join(url_list) + '/'
    return url


def get_testcase_from_txt():
    """读取txt文件：将txt内容转成list格式返回。"""
    caseList = []
    caseListFile = os.path.join(readConfig.proDir, "caselist.txt")
    fb = open(caseListFile)
    for value in fb.readlines():
        data = str(value)
        if data != '' and not data.startswith("#"):
            caseList.append(data.replace("\n", ""))
    fb.close()
    return caseList


def exldataTostr(data):
    if type(data) == float:
        d = str(int(data))
    else:
        d = str(data)
    return d


if __name__ == "__main__":
    # print(get_xls("signCase.xlsx", "event"))
    # set_visitor_token_to_config()
    # productInfo_xls = get_xls("signCase.xlsx", "event")
    # print(productInfo_xls)
    # xml = get_url_from_xml('event_get')
    # print(xml)
    # js = {"info": {'a': {'b': "bbb"}}, "b": '1', "a": '2'}
    # v = get_value_from_return_json(js, 'a', 'b')
    # print(v)
    # txt = get_testcase_from_txt()
    # print(txt)
    j = {'status': 200, 'message': 'success', 'data': {'eid': 1, 'name': '红米Pro发布会', 'limit': 2000,
                                                       'status': True, 'address': '北京会展中心',
                                                       'start_time': '2018-09-29T09:52:19.871'}}
    i = {'status': 200, 'message': 'success', 'data': [{'eid': 1, 'name': '红米Pro发布会'}]}

    v = get_value_from_return_json(i, 'data', 'name')
    print(v)
    # print(j['data'])
