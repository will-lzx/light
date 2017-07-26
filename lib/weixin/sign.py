import time
import random
import string
from wechatpy import WeChatClient
from light.settings import *


class Sign:
    def __init__(self, jsapi_ticket, url):
        self.ret = {
            'noncestr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        client = WeChatClient(WEIXIN_APPID, WEIXIN_APPSECRET)

        signature = client.jsapi.get_jsapi_signature(
            self.ret['noncestr'],
            self.ret['jsapi_ticket'],
            self.ret['timestamp'],
            self.ret['url']
        )
        return signature

if __name__ == '__main__':
    # 注意 URL 一定要动态获取，不能 hardcode
    sign = Sign('jsapi_ticket', 'http://relalive.com/weixin/wx/')
    print(sign.sign())
    print('')
