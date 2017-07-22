from light.settings import *
import urllib.request
import urllib.parse
import json
from lib.utils.sql_help import *


class UrlRequest:
    appID = WEIXIN_APPID
    appSecret = WEIXIN_APPSECRET
    access_token = ''

    def __init__(self):
        mysql = MySQL()
        access_token = mysql.get_accecc_token()
        self.access_token = access_token

    def url_request(self, url, params=None):
        if params:
            req = urllib.request.Request(url, params)
        else:
            req = urllib.request.Request(url, params)
        res = urllib.request.urlopen(req)
        urlResp = json.loads(res.read())
        return urlResp

    def get_menu(self):
        url = 'https://api.weixin.qq.com/cgi-bin/menu/get?access_token={0}'.format(self.access_token)
        return self.url_request(url)

    def create_menu(self):
        menu = {
            "button": [
                {
                    "name": "自拍杆",
                    "sub_button": [
                        {
                            "type": "view",
                            "name": "借自拍杆",
                            "url": "http://relalive.com/weixin/lend/"
                        },
                        {
                            "type": "view",
                            "name": "还自拍杆",
                            "url": "http://relalive.com/weixin/return_back/"
                        }]
                },
                {
                    "type": "view",
                    "name": "附近网点",
                    "url": "http://relalive.com/weixin/nearby/"

                },
                {
                    "name": "更多",
                    "sub_button": [
                        {
                            "type": "view",
                            "name": "个人中心",
                            "url": "http://relalive.com/weixin/privatecenter/"
                        },
                        {
                            "type": "view",
                            "name": "在线客服",
                            "url": "http://relalive.com/weixin/privatecenter/"
                        }]
                }]
        }
        data = json.dumps(menu, ensure_ascii=False)

        url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token={0}'.format(self.access_token)
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        req.add_header('encoding', 'utf-8')
        res = urllib.request.urlopen(req, data.encode())
        urlResp = json.loads(res.read())
        print(urlResp)


if __name__ == '__main__':
    url_request = UrlRequest()
    url_request.create_menu()


