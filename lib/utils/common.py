import random
import string
import time

from wechatpy import WeChatClient, WeChatOAuth
from light.settings import *
from lib.utils.url_request import *


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
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code'.format(WEIXIN_APPID, WEIXIN_APPSECRET, code)

    url_req = UrlRequest()
    resp = url_req.url_request(url)
    return resp['openid']


def get_prepare_id(appid, mch_id, nonceStr, sign, body, out_trade_no, total_fee, spbill_create_ip, notify_url, ):


def oauth(url):
    oAuth = WeChatOAuth(WEIXIN_APPID, WEIXIN_APPSECRET, url)
    return oAuth.authorize_url


if __name__ == '__main__':
    s = create_timestamp()
    get_openid()
    print('')
