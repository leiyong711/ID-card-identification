# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: ID-card-identification
# author: "Lei Yong" 
# creation time: 2017/6/30 0030 19:00
# Email: leiyong711@163.com
import time
import urllib2
import json

data = []


def id_card(filename):
    # 请求地址
    url = 'https://api-cn.faceplusplus.com/cardpp/v1/ocridcard'
    # 公钥
    key = "m_JZUUs-CzSzKsaqZa_TOAD7PMl4tv6r"
    # 密钥
    secret = "SqeJQDQ_ZBpKKwxJUEgpq0fv-FY6OS6N"
    # 参数协议分割标识
    boundary = '-%s' % hex(int(time.time() * 1000))

    # 制作协议包
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
    data.append(key)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
    data.append(secret)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"; filename="%s"' % ('image_file', filename))
    data.append('Content-Type: %s\r\n' % 'application/octet-stream')
    data.append(open(filename, 'rb').read())
    data.append('--%s--\r\n' % boundary)

    # Post请求
    http_body = '\r\n'.join(data)
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
    # print http_body
    req.add_data(http_body)
    resp = urllib2.urlopen(req, timeout=5)
    # 获取返回
    qrcont = resp.read()
    # print qrcont
    ps = json.loads(qrcont)
    ou = ps['cards']
    sd = ou[0]
    # print sd['side']
    if sd['side'] == 'front':
        side = u'人像面'
    else:
        side = u'国徽面'
    try:
        return u'签发机关：%s  有效期：%s\n身份证正反面：%s ' \
                % (sd['issued_by'], sd['valid_date'], side)
    except:
        return u'民族：%s    姓名：%s\n性别：%s    生日：%s\n身份证号：%s\n住址：%s\n身份证正反面：%s\n'\
             % (sd['race'], sd['name'], sd['gender'], sd['birthday'], sd['id_card_number'], sd['address'], side)


if __name__ == '__main__':
    print id_card('I:\\StudyTheCode\\shuax\\1.jpg')
