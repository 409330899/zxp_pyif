import sys
import time
import datetime
from configDB import DB
# sys.path.append('../db_fixture')


# 定义过去时间
past_time = time.strftime("%Y-%m-%d", time.localtime(time.time()-100000))

# 定义将来时间
future_time = time.strftime("%Y-%m-%d", time.localtime(time.time()+10000))
today = datetime.datetime.now()
tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)

# 测试数据准备
datas = {
    'sign_event':[
        {'id':1,'name':'红米Pro发布会','`limit`':2000,'status':1,'address':'北京会展中心',
         'start_time': tomorrow, 'create_time': tomorrow},
        {'id':2,'name':'可参加人数为0','`limit`':0,'status':1,'address':'北京会展中心',
         'start_time': tomorrow, 'create_time': future_time},
        {'id':3,'name':'当前状态为0关闭','`limit`':2000,'status':0,'address':'北京会展中心',
         'start_time':'2018-08-20 00:25:42','create_time': future_time},
        {'id':4,'name':'发布会已结束','`limit`':2000,'status':1,'address':'北京会展中心',
         'start_time':'2018-08-20 00:25:42','create_time': past_time},
        {'id':5,'name':'小米5发布会','`limit`':2000,'status':1,'address':'北京国家会议中心',
         'start_time':'2018-08-20 00:25:42','create_time': future_time},
        {'id':6,'name':'发布会已开始','`limit`':2000,'status':1,'address':'Beijing',
         'start_time':'2018-08-1','create_time': today},
    ],
    'sign_guest':[
        {'id':1,'realname':'alen','phone':1,'email':'alen@mail.com','sign':0,
         'create_time': '2018-12-20','event_id':1},
        {'id':2,'realname':'has sign','phone':2,'email':'sign@mail.com','sign':1,
         'create_time': '2018-12-20','event_id':2},
        {'id':3,'realname':'tom','phone':3,'email':'tom@mail.com','sign':0,
         'create_time': '2018-12-20','event_id':5},
    ],
}


# Inster table datas
def init_data():
    DB().init_data(datas)


if __name__ == '__main__':
    init_data()
