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
        tradeNo = create_order(user_id, out_trade_no, DEPOSIT, '押金支付')

        data = {
            'deposit': DEPOSIT,
            'tradeNo': tradeNo,
            'out_trade_no': out_trade_no
        }
        return render(request, 'zhifubao/pay.html', data)


@method_decorator(csrf_exempt)
def call_save_order(request):
    user_id = get_user_id(request)
    trade_no = request.POST.get('trade_no')
    out_trade_no = request.POST.get('out_trade_no')

    update_deposit(user_id, DEPOSIT, out_trade_no, False)

    save_order(user_id, out_trade_no, trade_no)

    return HttpResponse('success')


@method_decorator(csrf_exempt)
def call_return_order(request):
    user_id = get_user_id(request)
    trade_no = request.POST.get('trade_no')
    out_trade_no = request.POST.get('out_trade_no')

    update_lendhistorystatus(user_id, 2)

    save_order(user_id, out_trade_no, trade_no)

    return HttpResponse('success')


@method_decorator(csrf_exempt)
def get_pole(request):
    cabinet_code = request.POST.get('cabinet_code', None)
    print('cabinet_code', cabinet_code)
    has_pole = is_has_pole(cabinet_code)
    return HttpResponse(str(has_pole))


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


def lendhistory(request):
    template_name = 'zhifubao/lendhistory.html'
    user_id = get_user_id(request)

    histories = get_histories(user_id)

    cabinets = get_cabinets()

    rules = get_rules()

    spots = get_spots()

    lendtime = len(histories)

    deposit = float(get_deposit(user_id, is_weixin=False))

    context = {
        'lendhistory': histories,
        'lendtime': lendtime,
        'cabinets': cabinets,
        'spots': spots,
        'rules': rules,
        'deposit': deposit
    }

    response = render(request, template_name, context)
    return response


def privatecenter(request):
    template_name = 'zhifubao/privatecenter.html'

    #user_id, access_token = get_userid_access_token(auth_code)

    user_id = get_user_id(request)

    lendtime = get_lendtime(user_id)

    deposit = float(get_deposit(user_id, False))
    # user = get_userinfo(access_token, auth_code)

    headimgurl = request.session.get('avatar', default=None)
    nick_name = request.session.get('nick_name', default=None)

    if not headimgurl:
        headimgurl = ''
        nick_name = '亲爱的，轻拍用户'
    subscribe_time = get_subscribe_time(user_id)

    context = {
        'lendtime': lendtime,
        'deposit': deposit,
        'headimgurl': headimgurl,
        'nickname': nick_name,
        'subscribe_time': subscribe_time,
    }

    response = render(request, template_name, context)

    return response


class ReturnPayView(View):
    """
    wechat base pay view
    receive post data: order_id, price, title, notify_url, redirect_url
    ..remove WxMemberView
    """
    def get(self, request, *args, **kwargs):
        try:
            user_id = get_user_id(request)
            history = get_histories(user_id)[0]

            time_long = (history[3] - history[2]).seconds
            hour = time_long // 3600
            minute = round((time_long / 60) % 60, 0)

            lend_time_long = str(hour) + '时' + str(minute) + '分'

            money = get_pay_money(user_id)

        except KeyError:
            return HttpResponse("PARAM ERROR")

        out_trade_no = create_timestamp()
        tradeNo = create_order(user_id, out_trade_no, money, '租借费用支付')

        data = {
            'lend_money': money,
            'lend_time_long': lend_time_long,
            'order_id': out_trade_no,
            'lend_time': history[2],
            'return_time': history[3],
            'trade_no': tradeNo,
            'out_trade_no': out_trade_no
        }
        return render(request, 'zhifubao/return_pay.html', data)


def withdraw(request):
    template_name = 'zhifubao/withdraw.html'
    user_id = get_user_id(request)
    deposit = get_deposit(user_id, False)
    deposit_order_id = get_order_id(user_id, False)

    is_lend = is_lend_exist(user_id)

    is_payed = is_pay_finished(user_id)

    context = {
        'deposit': deposit,
        'deposit_order_id': deposit_order_id,
        'is_lend': is_lend,
        'is_pay_finished': is_payed
    }
    response = render(request, template_name, context)
    return response


@method_decorator(csrf_exempt)
def exe_withdraw(request):
    deposit = str(request.POST.get('deposit'))
    deposit_order_id = request.POST.get('deposit_order_id')
    user_id = get_user_id(request)

    resp_status = create_withdraw(deposit, deposit_order_id)

    if resp_status == 'Success':
        update_deposit(user_id, 0, 0, False)
    return HttpResponse(resp_status)


def buy_tip(request, lendhistory_id):
    template_name = 'zhifubao/buy_tip.html'

    history = get_lendhistory_by_id(lendhistory_id)

    lend_date = history[2]

    cabinets = get_cabinets()
    spot_id = 0
    for cabinet in cabinets:
        if cabinet[0] == history[7]:
            spot_id = cabinet[2]
    spots = get_spots()
    for spot in spots:
        if spot[0] == spot_id:
            lend_site = spot[1]

    context = {
        'lend_date': lend_date,
        'lend_site': lend_site
    }
    response = render(request, template_name, context)
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
    user_id = request.session.get('user_id', default=None)

    cabinet_id = get_cabinet_id(cabinet_code)

    rule_id = get_rule_id(cabinet_code)

    result = insert_lendhistory(user_id, rule_id, cabinet_id)

    return HttpResponse(result)


def lend_success(request):
    template_name = 'zhifubao/lend_success.html'

    response = render(request, template_name)
    return response


def contract(request):
    template_name = 'zhifubao/contract.html'
    response = render(request, template_name)
    return response


def about(request):
    template_name = 'zhifubao/about.html'
    response = render(request, template_name)
    return response


def use_help(request):
    template_name = 'zhifubao/use_help.html'
    response = render(request, template_name)
    return response


def deposit_question(request):
    template_name = 'zhifubao/help/deposit_question.html'
    response = render(request, template_name)
    return response


def get_fail(request):
    template_name = 'zhifubao/help/get_fail.html'
    response = render(request, template_name)
    return response


def how_return(request):
    template_name = 'zhifubao/help/how_return.html'
    response = render(request, template_name)
    return response


def how_use(request):
    template_name = 'zhifubao/help/how_to_use.html'
    response = render(request, template_name)
    return response


def lost(request):
    template_name = 'zhifubao/help/lost.html'
    response = render(request, template_name)
    return response


def several(request):
    template_name = 'zhifubao/help/several.html'
    response = render(request, template_name)
    return response


def how_pic(request):
    template_name = 'zhifubao/help/how_pic.html'
    response = render(request, template_name)
    return response


def how_charge(request):
    template_name = 'zhifubao/help/how_charge.html'
    response = render(request, template_name)
    return response


def call_back(request):
    code = request.GET.get('auth_code', None)
    print('code:', code)
    if code and not request.session.get('user_id', default=None):
        print('code', code)
        user_id = get_userid(code)
        request.session['user_id'] = user_id
    else:
        user_id = request.session.get('user_id', default=None)

    return HttpResponse(user_id)


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













