# import dingtalk.api
# request = dingtalk.api.OapiGettokenRequest("https://oapi.dingtalk.com/user/get")
# request.userid="userid1"
# response = request.getResponse()
# print(response)

import requests
import json
url = 'https://oapi.dingtalk.com/robot/send?access_token=d4a138bd691850b27bf4b7b67067bbb0f3e16a0c79ba03874cb87a94884a8d4b'

data ={
    "msgtype": "text", 
    "text": {
        "content": "我就是我, 是不一样的烟火"
    }

    # @群里的对象
    "at": {
        "atMobiles": [
        "18344579745",
        "13763050010",
    ], 
        "isAtAll": False
    }
} 

headers = {
    'Content-type':'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0'
}

re = requests.post(url,data=json.dumps(data),header = headers)         