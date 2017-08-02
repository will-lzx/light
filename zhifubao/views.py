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
from wechatpy.utils import to_text


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
        alipay_public_key_path="/root/zhifubao/alipay_public_key",
        sign_type="RSA2",
        debug=False
    )
    print('body', request.body)

    print('message', request.body)

    success = alipay.verify(request.body, sign)

    if success:
        return 'success'
    else:
        return 'fail'


def alipy_notify(request):
    print('notify')



