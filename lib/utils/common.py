import base64
import random
import string
import time

import datetime
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
    print('message:', message)
    key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhug73b3e2juIOIfxN7Ju2AMcwdOVqG4txOCea+r6nQBMyrlEIIbi1gKWFIbTCJAeKRhJPAZnApd8CCPGwSgRyxbYAUxJNF4BTIECTIHc0nXZVJASv6L0Miqnv7G2X1PFSWMlt4ijmo0f3mCnZONbk8MKcesSSN0EV5WfyJA/PUs+4rbJrEwCnoEtR6TgX+JPg+oa03/718T3jJGz4saWRH7QJD+jPFluZusy2LEMmckX+ZPusSpGZdEunqxbCoM8ywN+Ag2h9L6qOdj1VMTlzu/vweRyZDBW2ztWelbuzW7JRPrIGce0X0vomJ1ATEIPuCidaP16V6K+sguWsgNe8wIDAQAB'

    private_key = RSA.importKey(open('/root/zhifubao/app_private_key').read())
    #private_key = 'MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCUkAy5322rUVugNE4oyzK8kOkvMjJfVwltHL5jH7wLvSxDtIxfxlve3490Q/mXBy/EXfVKyd25ZkWP4WTH4dDB5fC5+CC/jP2aDt/Ex6RfF1eutladOT1MC6Y91H+ZXKdXh9LX/ZnMjh8r5yszXG0NvKZOmuVSj7cO6xRrNG9xZxN1Lg5Vh3OUBxW/Ux6sPjJhe0bzpYqCoHQRS1+dP11nRtVczFzuBQXcfdi48lLC+KjP4IBrG34QvZYsgNPCk5VwFae00TWfiU7YSG9I1nrw/gVd7LCTA+9QZIcYMi53SLh76Q3ryMNiPYsIwC/HsV2q3p0KzVzvrf3TNPgPfqilAgMBAAECggEAYiJhdaqkTAV7C/FhK8tGIY9rqVR0N8xLmrrg/KNq2SpGAhdSnrVt3GQ646c/SMdjg0g5jwSXpS9sheVyaCK/fkXA5WeFYmLk5o4qvFbQOkw2DF/ACS1VU1Vio/cpromotMYwvaJ0pM3Aw4R5Yf0MwIU8KjJhh08NshoRK9vAPdy9iJnTUVPTyyLl76p8rXHYePppZEUQUF3pr27NCwtTTgOyssZh8kH0Rm2ImWfNQ0nD7oTe6Be0wLJ5SN5wze0QKWssNFy0q0oHTemDoKvqVBp2WnRQBnNpEcb1Ahj7o1b68JBuyH/+1bXC3xquVPFPWO5oYlpunWS02AJ4/bKb4QKBgQDr4Eu6ljyzl3onvqUIIfbZJzCCat63gMfJHyzogDxVSWm6n6dbQwHVoc5wu26gKB3lFRq7eU6PNvC0TUmOfEVKTuT6o91dLI5QojEwwBNk9eO2XpktNm6Hp4Ejf06Y/fR3soLTKFNFuvy79setJds5SHxAq7HmwxJNRD8xDN8YeQKBgQChPMPusOjaDCJi5A/vqlgntZgwycNTcHZeK04nk/0ZMttC2l/V2fE85MT/AkK16nksXF7/Ih8sK8uOzCiNzRkmCx59Ci6gDWsb36SSsA3I6Rdxmn3hW47Zh0ObvstdJvNpliCaMIc9t/kRsrOUjuFJjI37jTvBWOj0I6V/AcAejQKBgQCAAMd36UHlwAVVfjr279+Stpa3n6Ffee5xcY6gWb7kFaPf1/YtK27abSWnvb9qAHtArzRDmrAMPidf4TVSspOzoJ7YeYaOorhUf8AsEYA04M+DT1DW3VwcF8WX6uVPVzmMn34pcw/FnpS6uFBh4VJXgsOTINm5PhE3hxq31qFXGQKBgBFf0OUpnw3P/OyXEriKrJEq2kl3lFqrZbXkCLnvEnjiqAneKjGLGJmtNSUdgz7DE2eaVIo9jQpfdcHfcgdFsI4O6Kwkqr2IdKA+SyebXQDnTSVqtmHQUeZS0xA3UQaqqdQY305+KDSYXHhxvzQk6VXZlXsjzuqYwBF+vdifwaoJAoGAbX11wE0h9kjU1RocZ6MfMtZ2AZRdP8LfrQSzh8mLxlR++2iB0ttX79wcVKrmfgKwc2FRPXrNWKI109pjtM8XVBScg8O+p1uZOXlePedViEnrf62NFA6a2/9FvOFWDRm7z6YgcCYk6NvUI3f9bPO3yYfhCvwLDhCG476hhOPU6qI='
    signer = PKCS1_v1_5.new(private_key)
    digest = SHA256.new()
    digest.update(message.encode("utf8"))
    sign_str = base64.b64encode(signer.sign(digest))

    print('sign_str', sign_str)
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
