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
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from lib.utils.common import *
from lib.weixin.weixin_sql import *
from alipay import AliPay


def lend(request):
    user_id = get_user_id(request)
    template_name = 'zhifubao/lend.html'

    is_deposit = is_deposit_exist(user_id, is_weixin=False)
    is_lend = is_lend_exist(user_id)

    context = {
        'is_deposit': is_deposit,
        'user_id': user_id,
        'is_lend': is_lend
    }

    response = render(request, template_name, context)
    return response


class PayView(View):
    """
    wechat base pay view
    receive post data: order_id, price, title, notify_url, redirect_url
    ..remove WxMemberView
    """
    def get(self, request, *args, **kwargs):
        user_id = get_user_id(request)
        out_trade_no = create_timestamp()
        tradeNo = create_order(user_id, out_trade_no)
        print('tradeNo:', tradeNo)
        # alipay = AliPay(
        #     appid=ALIPAY_APPID,
        #     app_notify_url="",
        #     app_private_key_path="/root/zhifubao/app_private_key",
        #     alipay_public_key_path="/root/zhifubao/alipay_public_key",
        #     sign_type="RSA2",
        #     debug=False
        # )
        # out_trade_no = create_timestamp()
        #order_string = alipay.api_alipay_trade_wap_pay(subject='押金支付', out_trade_no=out_trade_no, total_amount=DEPOSIT, return_url='/zhifubao/lend/')
        #
        # url = 'https://openapi.alipay.com/gateway.do?' + order_string
        # req = urllib.request.Request(order_string)
        # res = urllib.request.urlopen(req)
        # urlResp = json.loads(res.read())
        data = {
            'deposit': DEPOSIT,
            'tradeNo': tradeNo,
            'out_trade_no': out_trade_no
        }
        return render(request, 'zhifubao/pay.html', data)


def call_save_order(request):
    user_id = get_user_id(request)
    trade_no = request.POST.get('trade_no')
    out_trade_no = request.POST.get('out_trade_no')

    update_deposit(user_id, DEPOSIT, out_trade_no)

    save_order(user_id, out_trade_no, trade_no)

    template_name = 'zhifubao/return.html'

    response = render(request, template_name)
    return response


@method_decorator(csrf_exempt)
def update_lendhistory(request):
    user_id = request.POST.get('user_id', None)

    result = update_history(user_id)

    money = get_pay_money(user_id)

    if int(money) == 0:
        need_pay = 'False'
    else:
        need_pay = 'True'
    return HttpResponse(str(result) + '&' + need_pay)


def return_back(request):
    template_name = 'zhifubao/return.html'

    user_id = get_user_id(request)
    is_lend = is_lend_exist(user_id)
    context = {
        'user_id': user_id,
        'is_lend': is_lend
    }

    response = render(request, template_name, context)
    return response


def return_tip(request, has_capacity, cabinet_code):
    template_name = 'zhifubao/return_tip.html'

    user_id = get_user_id(request)

    context = {
        'has_capacity': has_capacity,
        'cabinet_code': cabinet_code,
        'user_id': user_id
    }

    response = render(request, template_name, context)
    return response


def nearby(request):
    template_name = 'zhifubao/nearby.html'
    response = render(request, template_name)
    return response


def privatecenter(request):
    template_name = 'zhifubao/privatecenter.html'

    response = render(request, template_name)
    return response


def output_tip(request, has_pole, cabinet_code):
    template_name = 'zhifubao/output_tip.html'
    context = {
        'has_pole': has_pole,
        'cabinet_code': cabinet_code
    }
    response = render(request, template_name, context)
    return response


@method_decorator(csrf_exempt)
def generate_lendhistory(request):

    cabinet_code = request.POST.get('cabinet_code', None)
    openid = request.session.get('openid', default=None)

    # cabinet_id = get_cabinet_id(cabinet_code)
    #
    # rule_id = get_rule_id(cabinet_code)
    #
    # result = insert_lendhistory(openid, rule_id, cabinet_id)

    return HttpResponse('')


def lend_success(request):
    template_name = 'zhifubao/lend_success.html'

    response = render(request, template_name)
    return response


def call_back(request):
    code = request.GET.get('auth_code', None)

    if code and not request.session.get('user_id', default=None):
        print('code', code)
        user_id = get_userid(code)
        request.session['user_id'] = user_id
    else:
        user_id = request.session.get('user_id', default=None)

    return user_id


def get_user_id(request):
    auth_code = request.GET.get('auth_code', None)

    if auth_code and not request.session.get('user_id', default=None):
        print('auth_code', auth_code)
        user_id = get_userid(auth_code)
        print('user_id', user_id)
        request.session['user_id'] = user_id
    else:
        user_id = request.session.get('user_id', default=None)

    return user_id













