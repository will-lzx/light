import hashlib
import json
import types
from ast import literal_eval
from collections import OrderedDict
from xml.etree import ElementTree

from alipay import AliPay
import xmltodict
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from past.types import unicode


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
    sign = request.POST.get('sign', None)
    print('sign', sign)
    alipay = AliPay(
        appid="2017072707914385",
        app_notify_url="http://relalive.com/zhifubao/alipy_notify/",
        app_private_key_path="/root/zhifubao/app_private_key",
        alipay_public_key_path="/root/zhifubao//root/zhifubao/",
        sign_type="RSA2",
        debug=False
    )

    data = {}
    data['sign_type'] = request.POST.get('sign_type')
    data['service'] = request.POST.get('service')
    data['charset'] = request.POST.get('charset')
    data['biz_content'] = request.POST.get('biz_content')

    success = alipay.verify(request.body, sign)
    if success:
        print("trade succeed")


def alipy_notify(request):
    alipay = request.registry['alipay']
    xml_dict = {}
    x = ElementTree.fromstring(alipay)
    print(x)
    xml_dict['appid'] = x.find('appid').text
    xml_dict['attach'] = x.find('attach').text
    xml_dict['bank_type'] = x.find('bank_type').text
    xml_dict['cash_fee'] = x.find('cash_fee').text
    xml_dict['fee_type'] = x.find('fee_type').text
    xml_dict['is_subscribe'] = x.find('is_subscribe').text
    xml_dict['mch_id'] = x.find('mch_id').text
    xml_dict['nonce_str'] = x.find('nonce_str').text
    xml_dict['openid'] = x.find('openid').text
    xml_dict['out_trade_no'] = x.find('out_trade_no').text
    xml_dict['result_code'] = x.find('result_code').text
    xml_dict['return_code'] = x.find('return_code').text
    xml_dict['sign'] = x.find('sign').text
    xml_dict['time_end'] = x.find('time_end').text
    xml_dict['total_fee'] = x.find('total_fee').text
    xml_dict['trade_type'] = x.find('trade_type').text
    xml_dict['transaction_id'] = x.find('transaction_id').text

    sign = xml_dict.pop('sign')
    if sign == generate_sign2(xml_dict):
        return True, xml_dict
    else:
        return False


def generate_sign2(sign_dict):
    ''' 生成签名, 目前只支持MD5签名 '''

    params_dict = OrderedDict(sorted(sign_dict.items(),
                              key=lambda t: t[0]))
    params_dict['key'] = ''
    print('params_dict', params_dict)
    foo_sign = []
    for k in params_dict:
        if isinstance(params_dict[k], unicode):
            params_dict[k] = params_dict[k].encode('utf-8')
        foo_sign.append('%s=%s' % (k, params_dict[k], ))
    foo_sign = '&'.join(foo_sign)
    sign = hashlib.md5(foo_sign).hexdigest().upper()
    return sign
