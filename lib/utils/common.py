import random
import string
import time

from wechatpy import WeChatClient, WeChatOAuth
from light.settings import *


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


def get_openid():
    client = WeChatClient(WEIXIN_APPID, WEIXIN_APPSECRET)

    usr = client.user.get('openid')

    print(usr)


def oauth(url):
    oAuth = WeChatOAuth(WEIXIN_APPID, WEIXIN_APPSECRET, url)
    oauth_url = oAuth.authorize_url()
    print('oauth', oauth_url)


if __name__ == '__main__':
    s = create_timestamp()
    get_openid()
    print('')
