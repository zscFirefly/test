# -*- coding:utf-8 -*-
import requests
import re
import pandas as pd
import psycopg2
import json
import sys
import datetime
reload(sys)
sys.setdefaultencoding('utf-8')



def get_content():
    conn = psycopg2.connect(database="store_production", user="rcdw", password="jintianzlk0706", host="10.10.9.21", port="5432")
    # conn = psycopg2.connect(database="store_production", user="rcdw", password="jintianzlk0706", host="121.46.31.61",port="50626")
    cur = conn.cursor()
    sql1 = '''
	with q as
	(SELECT 
	sd.name || '3小时内新增'|| count(distinct o.order_no)||'个携程订单' "content"
	from "public".orders o
	join "public".store_details sd on sd.id = o.store_id
	where o.booking_at between now() - interval '180 minutes 5 seconds' and now()
	and sd.store_type = 'ZYD'
	and o.source = 5
	GROUP BY sd.name
	)
	SELECT e'0携程渠道新增订单提醒：\n'||string_agg(q.content,e'\n') FROM q
    '''
    cur.execute(sql1)
    results = cur.fetchall()[0][0]
    return results


#给用户发送工作通知
def sent_messge(access_token,content):
    #content = 'test'
    url = 'https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2?access_token=' + access_token
    _data = {
            'agent_id':'26145755',
            # 'userid_list':'01461334659866',
            'userid_list':'153813615436554842',
            'msg':{
                    'msgtype':'text',
                    'text':{'content':content}}
            }
    headers = {'Content-Type': 'application/json;charset=utf-8'}

    data=json.dumps(_data, ensure_ascii=False) # 两种方式
    # data = '%s'%_data # 将json数据转化为str 否则报错
    
    response = requests.post(headers=headers,url=url,data=data.encode('utf-8'))
    result = response.json()
    print(result)

def get_access_token():
    url = 'https://oapi.dingtalk.com/gettoken?'\
    +'corpid=dingf920ee66623473bb&corpsecret='\
    +'S-QuWHG_0YG1zfuCzGZC0aybkUlDMQZYy1i7Mp1pCBi6EeaWZn6QZG3NPjPxbhM0'
    res = requests.get(url)
    access_token = re.findall(r'"access_token":"(.*?)"',res.text)[0]
    return access_token

def main():
    now=datetime.datetime.now()
    print("执行成功: "+str(now))
    content = get_content()
    access_token = get_access_token()
    sent_messge(access_token,content)


if __name__ == '__main__':
    main()