import base64
import random
import string
import time

import datetime

from urllib.parse import quote, quote_plus

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
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
    urlResp = get_oauth_response(code)
    user_id = urlResp['alipay_system_oauth_token_response']['user_id']

    return user_id


def get_userid_access_token(code):
    urlResp = get_oauth_response(code)
    user_id = urlResp['alipay_system_oauth_token_response']['user_id']
    access_token = urlResp['alipay_system_oauth_token_response']['access_token']

    return user_id, access_token


def get_userinfo(access_token, code):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    app_id = ALIPAY_APPID
    sign_type = 'RSA2'
    version = '1.0'
    grant_type = 'authorization_code'
    method = 'alipay.user.info.share'

    data = {'timestamp': timestamp,
            'app_id': app_id,
            'sign_type': sign_type,
            'version': version,
            'grant_type': grant_type,
            'method': method,
            'charset': 'GBK',
            'auth_token': access_token
            }
    unsigned_items = ordered_data(data)
    quoted_string = "&".join("{}={}".format(k, quote_plus(v)) for k, v in unsigned_items)

    print('quoted_string:', quoted_string)

    sign_str = sign(quoted_string.encode(encoding='utf-8')).decode()

    signed_string = quoted_string + "&sign=" + quote_plus(sign_str)

    req = requests.get('https://openapi.alipay.com/gateway.do?' + signed_string)

    print('req::', req.text)

    return req.json()['alipay_user_info_share_response']


def get_oauth_response(code):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    app_id = ALIPAY_APPID
    sign_type = 'RSA2'
    version = '1.0'
    grant_type = 'refresh_token'
    method = 'alipay.system.oauth.token'

    data = {'timestamp': timestamp,
            'app_id': app_id,
            'sign_type': sign_type,
            'version': version,
            'grant_type': grant_type,
            'method': method,
            'charset': 'GBK',
            #'code': code,
            'refresh_token': 'authusrB0d120cff349b47e891f3698a631f8E70'
            }
    unsigned_items = ordered_data(data)
    message = "&".join("{}={}".format(k, v) for k, v in unsigned_items)

    print('quoted_string:', message)

    sign_str = sign(message.encode(encoding='utf-8')).decode()

    quoted_string = "&".join("{}={}".format(k, quote_plus(v)) for k, v in unsigned_items)

    signed_string = quoted_string + "&sign=" + quote_plus(sign_str)

    req = requests.get('https://openapi.alipay.com/gateway.do?' + signed_string)
    print('reqqqqq:', req.json())

    return req.json()


def create_order(buy_id, out_trade_no):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    app_id = ALIPAY_APPID
    sign_type = 'RSA2'
    version = '1.0'
    method = 'alipay.trade.create'
    charset = 'GBK'

    goods_detail = [{
        "goods_id": "pole-1",
        "goods_name": "自拍杆",
        "quantity": 1,
        "price": 49,
    }]

    biz_content = {'body': '押金支付',
                   'subject': '押金支付',
                   'buyer_id': buy_id,
                   'out_trade_no': out_trade_no,
                   'timeout_express': '90m',
                   'total_amount': DEPOSIT,
                   'goods_detail': goods_detail
                   }

    data = {'timestamp': timestamp,
            'app_id': app_id,
            'sign_type': sign_type,
            'version': version,
            'method': method,
            'biz_content': biz_content,
            'charset': charset
            }
    unsigned_items = ordered_data(data)
    message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)

    sign_str = sign(message.encode(encoding='utf-8')).decode()

    quoted_string = "&".join("{}={}".format(k, quote_plus(v)) for k, v in unsigned_items)

    signed_string = quoted_string + "&sign=" + quote_plus(sign_str)

    req = requests.get('https://openapi.alipay.com/gateway.do?' + signed_string)

    return req.json()['alipay_trade_create_response']['trade_no']


def create_withdraw(deposit, out_trade_no):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    app_id = ALIPAY_APPID
    sign_type = 'RSA2'
    version = '1.0'
    method = 'alipay.trade.refund'
    charset = 'GBK'

    biz_content = {'out_trade_no': out_trade_no,
                   'refund_amount': deposit
                   }

    data = {'timestamp': timestamp,
            'app_id': app_id,
            'sign_type': sign_type,
            'version': version,
            'method': method,
            'biz_content': biz_content,
            'charset': charset
            }
    unsigned_items = ordered_data(data)
    message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)

    sign_str = sign(message.encode(encoding='utf-8')).decode()

    quoted_string = "&".join("{}={}".format(k, quote_plus(v)) for k, v in unsigned_items)

    signed_string = quoted_string + "&sign=" + quote_plus(sign_str)

    req = requests.get('https://openapi.alipay.com/gateway.do?' + signed_string)

    return req.json()['alipay_trade_refund_response']['msg']


def get_subscribe_time(user_id):
    mysql = MySQL(db='management')
    subcribe_time = mysql.exec_query(
        'select create_time from home_customer where alipay="{0}"'.format(user_id))[0][0]
    return subcribe_time


def oauth(url):
    oAuth = WeChatOAuth(WEIXIN_APPID, WEIXIN_APPSECRET, url)
    return oAuth.authorize_url


def get_rule_id(cabinet_code):
    mysql = MySQL(db='management')
    rule_id = mysql.exec_query(
        'select rule_id from home_spot where id=(select spot_id from home_cabinet where number="{0}")'.format(
            cabinet_code))[0][0]
    return rule_id


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
