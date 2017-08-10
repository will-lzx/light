import hashlib
import json
import re
from collections import OrderedDict

import xmltodict
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from alipay import AliPay
from light.settings import *


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
    args = request.POST

    for k, v in args.items():
        args[k] = v[0]

    check_sign = params_to_string(args)

    params = string_to_dict(check_sign)

    sign = params['sign']

    params = params_filter(params)

    signature_str = params_to_verify_string(params, quotes=False, reverse=False)

    check_res = check_ali_sign(signature_str, sign)
    if not check_res:
        res = 'fail'
    res = verify_from_gateway({"partner": ALIPAY_PARTNERID, "notify_id": params["notify_id"]})

    if not res:
        res = 'fail'

    if res != 'fail':
        return 'success'
    else:
        return res


def check_ali_sign(signature, sign):
    return signature == sign


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
        if key == "sign" or key == "sign_type" or value == "":
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
    cafile = 'cacert.pem'
    res = requests.get(ali_gateway_url, verify=cafile)
    if res.text == "true":
        return True
    return False





