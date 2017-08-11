import hashlib
import json
import re
import urllib.request
from base64 import decodebytes
from collections import OrderedDict

import xmltodict
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from alipay import AliPay
from light.settings import *
import requests


def lend(request):
    template_name = 'zhifubao/lend.html'

    response = render(request, template_name)
    return response


def return_back(request):
    template_name = 'zhifubao/return.html'

    response = render(request, template_name)
    return response


def nearby(request):
    template_name = 'zhifubao/nearby.html'
    response = render(request, template_name)
    return response


def privatecenter(request):
    template_name = 'zhifubao/privatecenter.html'

    response = render(request, template_name)
    return response


@csrf_exempt
def zfb(request):
    alipay = AliPay(
        appid="2017072707914385",
        app_notify_url="http://relalive.com/zhifubao/alipy_notify/",
        app_private_key_path="/root/zhifubao/app_private_key",
        alipay_public_key_path="/root/zhifubao/alipay_public_key",
        sign_type="RSA2",
        debug=False
    )

    res = {}
    arguments = {}
    #args = request.body.decode("gb2312").split('&')
    args = request.body.split('&')
    print('args:', args)
    for item in args:
        k = item.split('=', 1)[0]
        v = item.split('=', 1)[1]
        arguments[k] = v

    check_sign = params_to_string(arguments)

    params = string_to_dict(check_sign)

    sign = params['sign']

    params = params_filter(params)

    signature_str = params_to_verify_string(params, quotes=False, reverse=False)

    print('signature_str', signature_str)
    # check_res = check_ali_sign(signature_str, sign)
    check_res = alipay.verify(signature_str, sign)
    if not check_res:
        res = 'fail'
    print('res1:', res)
    res = verify_from_gateway({"partner": ALIPAY_PARTNERID, "notify_id": params["notify_id"]})

    if not res:
        res = 'fail'

    if res != 'fail':
        return 'success'
    else:
        return res


def check_ali_sign(signature, sign):
    with open('/root/alipay_public_key.pem') as fp:
        alipay_public_key = RSA.importKey(fp.read())

    print('alipay_public_key', alipay_public_key)

    from alipay import AliPay
    alipay = AliPay()
    alipay.verify()

    alipay_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhug73b3e2juIOIfxN7Ju2AMcwdOVqG4txOCea+r6nQBMyrlEIIbi1gKWFIbTCJAeKRhJPAZnApd8CCPGwSgRyxbYAUxJNF4BTIECTIHc0nXZVJASv6L0Miqnv7G2X1PFSWMlt4ijmo0f3mCnZONbk8MKcesSSN0EV5WfyJA/PUs+4rbJrEwCnoEtR6TgX+JPg+oa03/718T3jJGz4saWRH7QJD+jPFluZusy2LEMmckX+ZPusSpGZdEunqxbCoM8ywN+Ag2h9L6qOdj1VMTlzu/vweRyZDBW2ztWelbuzW7JRPrIGce0X0vomJ1ATEIPuCidaP16V6K+sguWsgNe8wIDAQAB'
    key = alipay_public_key
    print('key:', key)
    signer = PKCS1_v1_5.new(key)
    digest = SHA256.new()



    digest.update(signature.encode("utf8"))
    if signer.verify(digest, decodebytes(sign.encode("utf8"))):
        return True
    else:
        return False


def alipy_notify(request):
    print('notify')


def params_to_string(params, quotes=False, reverse=False):
    query = ''
    for key in sorted(params.keys(), reverse=reverse):
        value = params[key]
        if quotes:
            query += str(key) + '=\"' + str(value) + '\"&'
        else:
            query += str(key) + "=" + str(value) + "&"
    query = query[0:-1]
    return query


def string_to_dict(query):
    res = {}
    k_v_pairs = query.split('&')
    for item in k_v_pairs:
        sp_item = item.split('=', 1)
        key = sp_item[0]
        value = sp_item[1]
        res[key] = value
    return res


def params_filter(params):
    ret = {}
    for key, value in params.items():
        if key == "sign" or value == "":
            continue
        ret[key] = value
    return ret


def params_to_verify_string(params, quotes=False, reverse=False):
    query = ''
    for key in sorted(params.keys(), reverse=reverse):
        value = params[key]
        if quotes:
            query += str(key) + "=\"" + str(value) + "\"&"
        else:
            query += str(key) + "=" + str(value) + "&"
    query = query[0:-1]
    return query


def verify_from_gateway(params_dict):
    ali_gateway_url = "https://mapi.alipay.com/gateway.do?service=notify_verify&partner=%(partner)d&notify_id=%(notify_id)s"
    notify_id = params_dict["notify_id"]
    partner = ALIPAY_PARTNERID
    ali_gateway_url = ali_gateway_url % {"partner": partner, "notify_id": notify_id}
    cafile = '/root/cacert.pem'
    res = requests.get(ali_gateway_url, cert=(cafile,))
    if res.text == "true":
        return True
    return False





