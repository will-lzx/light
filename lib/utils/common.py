import random
import string
import time

from wechatpy import WeChatClient, WeChatOAuth
from light.settings import *
from lib.utils.url_request import *
from lib.utils.sql_help import *


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


def oauth(url):
    oAuth = WeChatOAuth(WEIXIN_APPID, WEIXIN_APPSECRET, url)
    return oAuth.authorize_url


def get_rule_id(cabinet_code):
    mysql = MySQL(db='management')
    rule_id = mysql.exec_query('select rule_id from home_spot where id=(select spot_id from home_cabinet where number="{0}")'.format(cabinet_code))[0][0]
    return rule_id


if __name__ == '__main__':
    # s = create_timestamp()
    # get_openid()
    rule_id = get_rule_id('12-1213-21')
    print(rule_id)
