# encoding:utf-8


'''
驾驶行为分析
'''


def getFiveSocre():
    import base64
    import json
    import urllib
    
    from urllib import request
    from urllib import parse
    from urllib.request import urlopen
    # 驾驶行为分析
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/driver_behavior"
    # 二进制方式打开图片文件
    f = open('img/peopleCM.jpg', 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    params = parse.urlencode(params).encode('utf-8')

    def getTokenBaidu():
        host = 'https://aip.baidubce.com/oauth/2.0/token?'
        param = 'grant_type=client_credentials&client_id=cpNVj72BSkKI3xKb6t8OxgYB&client_secret=iHF24EdTcC1wM3qs9V6loHhYpA6N1xzX'
        params = host + param
        req = request.Request(params)
        req.add_header('Content-Type', 'application/json; charset=UTF-8')
        response = request.urlopen(req)
        content = response.read()
        return json.loads(content)['access_token']

    # access_token 每个月更新一次
    access_token = getTokenBaidu()
    request_url = request_url + "?access_token=" + access_token
    request = request.Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = urlopen(request)
    content = response.read()
    content = json.loads(content)

    # to output result of computing.
    person_num = content['person_num']

    if person_num > 0:
        result = {
            'cellphone': content['person_info'][0]['attributes']['cellphone'],
            'both_hands_leaving_wheel': content['person_info'][0]['attributes']['both_hands_leaving_wheel'],
            'not_facing_front': content['person_info'][0]['attributes']['not_facing_front'],
            'not_buckling_up': content['person_info'][0]['attributes']['not_buckling_up'],
            'smoke': content['person_info'][0]['attributes']['smoke']
        }
        return result
    else:
        return None
