import random
import string
import time

import datetime
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from wechatpy import WeChatClient, WeChatOAuth
from light.settings import *
from lib.utils.url_request import *
from lib.utils.sql_help import *
import requests
from lib.utils.get_sign import sign


def create_nonce_str():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))


def create_timestamp():
    return int(time.time())


def get_signature(noncestr, jsapi_ticket, timestamp, url):
    client = WeChatClient(WEIXIN_APPID, WEIXIN_APPSECRET)

    signature = client.jsapi.get_jsapi_signature(
        noncestr,
        jsapi_ticket,
        timestamp,
        url
    )
    return signature


def get_openid(code):
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code'.format(
        WEIXIN_APPID, WEIXIN_APPSECRET, code)

    url_req = UrlRequest()
    resp = url_req.url_request(url)
    return resp['openid']


def get_userid(code):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    app_id = ALIPAY_APPID
    sign_type = 'RSA2'
    version = '1.0'
    grant_type = 'authorization_code'
    method = 'alipay.system.oauth.token'

    data = {'timestamp': timestamp,
            'app_id': app_id,
            'sign_type': sign_type,
            'version': version,
            'grant_type': grant_type,
            'method': method
            }
    unsigned_items = ordered_data(data)
    message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)

    sign_str = sign(message.encode(encoding="utf-8"))
    url = 'https://openapi.alipay.com/gateway.do?timestamp={0}&method=alipay.system.oauth.token&app_id={1}' \
          '&sign_type=RSA2&sign={2}&version=1.0&grant_type=authorization_code&code={3}'.format(timestamp, app_id, sign_str,
                                                                                               code)

    print('url:', url)
    resp = requests.get(url)
    print('resp', resp.json)
    return resp.content


def oauth(url):
    oAuth = WeChatOAuth(WEIXIN_APPID, WEIXIN_APPSECRET, url)
    return oAuth.authorize_url


def get_rule_id(cabinet_code):
    mysql = MySQL(db='management')
    rule_id = mysql.exec_query(
        'select rule_id from home_spot where id=(select spot_id from home_cabinet where number="{0}")'.format(
            cabinet_code))[0][0]
    return rule_id


def create_sign():
    from alipay import AliPay
    alipy = AliPay()
    alipy.verify()

    alipay_public_key = ''
    key = alipay_public_key
    signer = PKCS1_v1_5.new(key)
    digest = SHA256.new()
    digest.update(message.encode("utf8"))


def ordered_data(data):
    complex_keys = []
    for key, value in data.items():
        if isinstance(value, dict):
            complex_keys.append(key)

    # 将字典类型的数据dump出来
    for key in complex_keys:
        data[key] = json.dumps(data[key], separators=(',', ':'))

    return sorted([(k, v) for k, v in data.items()])


if __name__ == '__main__':
    # s = create_timestamp()
    # get_openid()
    rule_id = get_rule_id('12-1213-21')
    print(rule_id)
