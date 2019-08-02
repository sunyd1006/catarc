#!/usr/bin/env python
# coding: utf-8

import ssl
import json
import urllib
import sys
import base64
import urllib3
import os
from urllib import request, parse

'''
    人脸面部对比
'''

# # 1. 动态获取百度AI access_token
# client_id 为官网获取的AK， client_secret 为官网获取的SK


def getTokenBaidu():
    host = 'https://aip.baidubce.com/oauth/2.0/token?'
    param = 'grant_type=client_credentials&client_id=cpNVj72BSkKI3xKb6t8OxgYB&client_secret=iHF24EdTcC1wM3qs9V6loHhYpA6N1xzX'
    params = host + param
    req = request.Request(params)
    req.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = request.urlopen(req)
    content = response.read()
    return json.loads(content)['access_token']


# # 2. 从萤石获得accessToken 并截图保存至本地
# 获取accessToken
def getTokenYinshi():
    '''
        appKey:    记得及时在萤石开发者官网更新
        appSecret: 记得及时在萤石开发者官网更新
    '''
    accessTokenParam = parse.urlencode([
        ('appKey', '43fdd6d8aae743a89338f7ecdff2192e'),
        ('appSecret', '18b9543f4c658d37423b9e19b0ba4d2e')
    ])
    urlYS = 'https://open.ys7.com/api/lapp/token/get'
    with request.urlopen(urlYS, data=accessTokenParam.encode('utf-8')) as f:
        data = f.read().decode('utf-8')
        data = json.loads(data)
        tokenYinshi = data['data']['accessToken']
    return tokenYinshi


def downPicFromYinshi(token, path):
    '''
        获取截图url 并保存至本地
    '''
    param2 = parse.urlencode([
        ('accessToken', token),
        ('deviceSerial', 'D00303834'),
        ('channelNo', 1)
    ])
    urlCap = 'https://open.ys7.com/api/lapp/device/capture'
    with request.urlopen(urlCap, data=param2.encode('utf-8')) as f:
        try:
            data = f.read().decode('utf-8')
            data = json.loads(data)
            #  data['data']['picUrl'] 在萤石云服务器上的图片地址
            # 保存一帧图片到本地 import os
            print(data)
            request.urlretrieve(data['data']['picUrl'], filename=os.getcwd() + path)
        except Exception:
            return None


# # 3. 计算两张图片的相似度

# 获取相似度 picture1 picture2
def getScore(pic1, pic2):
    # 下载图片到某文件夹。
    path = './img/peopleCM.jpg'
    downPicFromYinshi(getTokenYinshi(), path)

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    http = urllib3.PoolManager()
    url = 'https://aip.baidubce.com/rest/2.0/face/v3/match?access_token=' + getTokenBaidu()

    # suncm.jpg 为摄像机抓拍到的图片
    f1 = open(pic1, 'rb')
    # sunGB 为数据库中的备份图片，这里将来要扩展
    f2 = open(pic2, 'rb')

    # 参数image：图像base64编码 分别base64编码后的2张图片数据
    img1 = base64.b64encode(f1.read())
    img2 = base64.b64encode(f2.read())
    params = [{"image": str(img1, 'utf-8'), "image_type": 'BASE64'},
              {"image": str(img2, 'utf-8'), "image_type": 'BASE64'}]

    # 参数转JSON格式
    encoded_data = json.dumps(params).encode('utf-8')

    request = http.request('POST',
                           url,
                           body=encoded_data,
                           headers={'Content-Type': 'application/json'})

    # 对返回的bytes字节进行处理。Python3输出位串，而不是可读的字符串，需要进行转换
    result = str(request.data, 'utf-8')
    result = json.loads(result)

    if result['error_code'] == 0:
        return result['result']['score']
    else:
        return -1


'''
调用方法：getSorce(pic1, pic2)
print(getScore('img/peopleCM.jpg', 'img/peopleGB.jpg'))
'''
