import xmltodict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from wechatpy.events import SubscribeEvent, LocationEvent
from wechatpy.pay.api import WeChatRefund
from lib.weixin.weixin_sql import *

from lib.utils.common import *
from wechatpy import parse_message, create_reply, WeChatPay
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException

from lib.utils.url_request import *
from weixin.wx_api import Pay as PayApi


# Create your views here.


def agreement(request):
    template_name = 'weixin/agreement.html'
    response = render(request, template_name)
    return response


def lend(request):
    template_name = 'weixin/lend.html'

    set_weixin_zhifubao(request)
    is_weixin = get_weixin_zhifubao(request)

    openid = get_open_id(request, is_weixin)

    is_deposit = is_deposit_exist(openid, is_weixin)
    is_lend = is_lend_exist(openid)
    is_payed = is_pay_finished(openid)

    context = {
        'is_deposit': is_deposit,
        'openid': openid,
        'is_lend': is_lend,
        'is_weixin': is_weixin,
        'is_pay_finished': is_payed
    }
    response = render(request, template_name, context)
    return response


@method_decorator(csrf_exempt)
def generate_lendhistory(request):

    cabinet_code = request.POST.get('cabinet_code', None)
    is_weixin = get_weixin_zhifubao(request)
    openid = get_open_id(request, is_weixin)

    cabinet_id = get_cabinet_id(cabinet_code)

    rule_id = get_rule_id(cabinet_code)

    result = insert_lendhistory(openid, rule_id, cabinet_id)

    return HttpResponse(result)


def lend_success(request):
    template_name = 'weixin/lend_success.html'

    response = render(request, template_name)
    return response


def return_back(request):
    template_name = 'weixin/return.html'

    set_weixin_zhifubao(request)
    is_weixin = get_weixin_zhifubao(request)

    openid = get_open_id(request, is_weixin)

    is_lend = is_lend_exist(openid)
    context = {
        'openid': openid,
        'is_lend': is_lend,
        'is_weixin': is_weixin
    }

    response = render(request, template_name, context)
    return response


@method_decorator(csrf_exempt)
def update_lendhistory(request):
    is_weixin = get_weixin_zhifubao(request)
    openid = get_open_id(request, is_weixin)

    result = update_history(openid)

    money = get_pay_money(openid)

    if int(money) == 0:
        need_pay = 'False'
    else:
        need_pay = 'True'
    return HttpResponse(str(result) + '&' + need_pay)


def return_tip(request, has_capacity, cabinet_code):
    template_name = 'weixin/return_tip.html'

    is_weixin = get_weixin_zhifubao(request)
    openid = get_open_id(request, is_weixin)

    context = {
        'has_capacity': has_capacity,
        'cabinet_code': cabinet_code,
        'openid': openid
    }

    response = render(request, template_name, context)
    return response


def get_pole(request):
    cabinet_code = request.POST.get('cabinet_code', None)
    has_pole = is_has_pole(cabinet_code)
    return HttpResponse(str(has_pole))


@method_decorator(csrf_exempt)
def get_capacity(request):
    cabinet_code = request.POST.get('cabinet_code', None)
    has_capacity = is_has_capacity(cabinet_code)
    return HttpResponse(str(has_capacity))


def output_tip(request, has_pole, cabinet_code):
    template_name = 'weixin/output_tip.html'
    context = {
        'has_pole': has_pole,
        'cabinet_code': cabinet_code
    }
    response = render(request, template_name, context)
    return response


def nearby(request):
    template_name = 'weixin/nearby.html'
    set_weixin_zhifubao(request)
    is_weixin = get_weixin_zhifubao(request)
    openid = get_open_id(request, is_weixin)

    cabinets = get_cabinets()

    lon = request.session.get('lon', None)
    print('lon::::', lon)

    if lon is None:
        lon = DEFAULT_LON

    lat = request.session.get('lat', None)
    if lat is None:
        lat = DEFAULT_LAT

    context = {
        'lon': lon,
        'lat': lat,
        'cabinets': cabinets
    }

    response = render(request, template_name, context)
    return response


def lendhistory(request):
    template_name = 'weixin/lendhistory.html'
    is_weixin = get_weixin_zhifubao(request)
    openid = get_open_id(request, is_weixin)

    histories = get_histories(openid)

    cabinets = get_cabinets()

    rules = get_rules()

    spots = get_spots()

    lendtime = len(histories)

    context = {
        'lendhistory': histories,
        'lendtime': lendtime,
        'cabinets': cabinets,
        'spots': spots,
        'rules': rules
    }

    response = render(request, template_name, context)
    return response


def withdraw(request):
    template_name = 'weixin/withdraw.html'

    is_weixin = get_weixin_zhifubao(request)
    openid = get_open_id(request, is_weixin)

    deposit = get_deposit(openid, is_weixin)
    deposit_order_id = get_order_id(openid, is_weixin)

    is_lend = is_lend_exist(openid)

    is_payed = is_pay_finished(openid)

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
    is_weixin = get_weixin_zhifubao(request)
    openid = get_open_id(request, is_weixin)

    deposit_order_id = request.POST.get('deposit_order_id')
    if is_weixin:
        deposit = str(int(float(request.POST.get('deposit')) * 100))

        refund_no = str(create_timestamp())
        wechatPay = WeChatPay(WEIXIN_APPID,
                              WECHAT[0]['key'],
                              WECHAT[0]['mch_id'],
                              mch_cert='/root/cert/apiclient_cert.pem',
                              mch_key='/root/cert/apiclient_key.pem')

        refund = WeChatRefund(wechatPay)

        resp = refund.apply(deposit, deposit, out_trade_no=deposit_order_id, out_refund_no=refund_no, op_user_id=WECHAT[0]['mch_id'])
        if resp['return_code'] == 'SUCCESS':
            update_deposit(openid, 0, 0, is_weixin)
        return HttpResponse(resp['return_code'])
    else:
        deposit = str(request.POST.get('deposit'))

        resp_status = create_withdraw(deposit, deposit_order_id)

        if resp_status == 'Success':
            update_deposit(openid, 0, 0, is_weixin)
        return HttpResponse(resp_status)


def buy_tip(request, lendhistory_id):
    template_name = 'weixin/buy_tip.html'

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


def use_help(request):
    template_name = 'weixin/use_help.html'
    response = render(request, template_name)
    return response


def deposit_question(request):
    template_name = 'weixin/help/deposit_question.html'
    response = render(request, template_name)
    return response


def get_fail(request):
    template_name = 'weixin/help/get_fail.html'
    response = render(request, template_name)
    return response


def how_return(request):
    template_name = 'weixin/help/how_return.html'
    response = render(request, template_name)
    return response


def how_use(request):
    template_name = 'weixin/help/how_to_use.html'
    response = render(request, template_name)
    return response


def lost(request):
    template_name = 'weixin/help/lost.html'
    response = render(request, template_name)
    return response


def several(request):
    template_name = 'weixin/help/several.html'
    response = render(request, template_name)
    return response


def how_pic(request):
    template_name = 'weixin/help/how_pic.html'
    response = render(request, template_name)
    return response


def how_charge(request):
    template_name = 'weixin/help/how_charge.html'
    response = render(request, template_name)
    return response


class PayView(View):
    """
    wechat base pay view
    receive post data: order_id, price, title, notify_url, redirect_url
    ..remove WxMemberView
    """
    def get(self, request, *args, **kwargs):
        is_weixin = get_weixin_zhifubao(request)
        openid = get_open_id(request, is_weixin)
        if is_weixin:
            try:
                price = DEPOSIT
                notify_url = WEIXIN_PAYBACK + '?price=' + str(DEPOSIT) + '&is_deposit=True'

                redirect_url = '/weixin/lend/'

            except KeyError:
                return HttpResponse("PARAM ERROR")

            out_trade_no = str(int(time.time()))
            total_fee = str(int(float(price) * 100))
            param = {
                'xml': {'openid': openid,
                        'body': WECHAT[0]['body'],
                        'out_trade_no': out_trade_no,
                        'total_fee': total_fee,
                        'spbill_create_ip': WEIXIN_IP,
                        'notify_url': notify_url}}
            pay = PayApi()
            pay.set_prepay_id(param)
            data = {
                'data': pay.get_pay_data(),
                'is_weixin': is_weixin,
                'redirect_uri': redirect_url,
                'deposit': price,
            }
            template_name = 'weixin/weixin_pay.html'
        else:
            out_trade_no = create_timestamp()
            tradeNo = create_order(openid, out_trade_no, DEPOSIT, '押金支付')

            data = {
                'deposit': DEPOSIT,
                'is_weixin': is_weixin,
                'tradeNo': tradeNo,
                'out_trade_no': out_trade_no,
            }
            template_name = 'weixin/zhifubao_pay.html'

        return render(request, template_name, data)


class ReturnPayView(View):
    """
    wechat base pay view
    receive post data: order_id, price, title, notify_url, redirect_url
    ..remove WxMemberView
    """
    def get(self, request, *args, **kwargs):

        is_weixin = get_weixin_zhifubao(request)
        openid = get_open_id(request, is_weixin)

        cabinets = get_cabinets()

        spots = get_spots()
        if is_weixin:
            try:

                history = get_histories(openid)[0]

                time_long = (history[3] - history[2]).seconds
                hour = time_long // 3600
                minute = round((time_long / 60) % 60, 0)

                lend_time_long = str(hour) + '时' + str(minute) + '分'

                money = get_pay_money(openid)
                notify_url = WEIXIN_RETURNPAYBACK + '?price=' + str(money) + '&is_deposit=False'
                redirect_url = '/weixin/privatecenter/'

            except KeyError:
                return HttpResponse("PARAM ERROR")

            out_trade_no = str(int(time.time()))

            total_fee = str(int(float(money) * 100))

            param = {
                'xml': {'openid': openid,
                        'body': '租借费用支付',
                        'out_trade_no': out_trade_no,
                        'total_fee': total_fee,
                        'spbill_create_ip': WEIXIN_IP,
                        'notify_url': notify_url}}
            pay = PayApi()
            pay.set_prepay_id(param)
            data = {
                'data': pay.get_pay_data(),
                'redirect_uri': redirect_url,
                'lend_money': money,
                'lend_time_long': lend_time_long,
                'order_id': out_trade_no,
                'lend_time': history[2],
                'return_time': history[3],
                'is_weixin': is_weixin,
                'cabinet_id': history[7],
                'cabinets': cabinets,
                'spots': spots
            }
            template_name = 'weixin/weixin_return_pay.html'
        else:
            try:
                history = get_histories(openid)[0]

                time_long = (history[3] - history[2]).seconds
                hour = time_long // 3600
                minute = round((time_long / 60) % 60, 0)

                lend_time_long = str(hour) + '时' + str(minute) + '分'

                money = get_pay_money(openid)

            except KeyError:
                return HttpResponse("PARAM ERROR")

            out_trade_no = create_timestamp()
            tradeNo = create_order(openid, out_trade_no, money, '租借费用支付')

            data = {
                'lend_money': money,
                'lend_time_long': lend_time_long,
                'order_id': out_trade_no,
                'lend_time': history[2],
                'return_time': history[3],
                'trade_no': tradeNo,
                'out_trade_no': out_trade_no,
                'is_weixin': is_weixin,
                'cabinet_id': history[7],
                'cabinets': cabinets,
                'spots': spots
            }
            template_name = 'weixin/zhifubao_return_pay.html'
        return render(request, template_name, data)


class WxPayNotifyView(View):
    """
    Receive wechat service data
    valid and send order_id, pay_number to notify_url
    """
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(WxPayNotifyView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        price = DEPOSIT
        pay = PayApi()
        data = request.body
        data = dict(xmltodict.parse(data)['xml'])
        result = {}
        sign = data['sign']
        del data['sign']
        if sign:
            total_fee = price
            openid = data['openid']
            order_id = data['out_trade_no']
            pay_number = data['transaction_id']

            update_deposit(openid, total_fee, order_id, True)

            save_order(openid, order_id, pay_number)
            result = self.handle_order(order_id, pay_number)
        else:
            result['return_code'] = 'FAIL'
            result['return_msg'] = 'ERROR'

        result_xml = pay.dict_to_xml(result)
        return HttpResponse(result_xml)

    def handle_order(self, order_id, pay_number):
        """ Need user extends, for order """
        return HttpResponse('<xml> <return_code><![CDATA[SUCCESS]]></return_code> <return_msg><![CDATA[OK]]></return_msg> </xml>')


class WxReturnPayNotifyView(View):
    """
    Receive wechat service data
    valid and send order_id, pay_number to notify_url
    """
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(WxReturnPayNotifyView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pay = PayApi()
        data = request.body
        data = dict(xmltodict.parse(data)['xml'])

        result = {}
        sign = data['sign']
        del data['sign']
        if sign:
            openid = data['openid']
            order_id = data['out_trade_no']
            pay_number = data['transaction_id']

            update_lendhistorystatus(openid, 2)

            save_order(openid, order_id, pay_number)
            result = self.handle_order(order_id, pay_number)
        else:
            result['return_code'] = 'FAIL'
            result['return_msg'] = 'ERROR'

        result_xml = pay.dict_to_xml(result)
        return HttpResponse(result_xml)

    def handle_order(self, order_id, pay_number):
        """ Need user extends, for order """
        return HttpResponse('<xml> <return_code><![CDATA[SUCCESS]]></return_code> <return_msg><![CDATA[OK]]></return_msg> </xml>')


@method_decorator(csrf_exempt)
def call_save_order(request):
    is_weixin = get_weixin_zhifubao(request)
    openid = get_open_id(request, is_weixin)

    trade_no = request.POST.get('trade_no')
    out_trade_no = request.POST.get('out_trade_no')

    update_deposit(openid, DEPOSIT, out_trade_no, is_weixin)

    save_order(openid, out_trade_no, trade_no)

    return HttpResponse('success')


@method_decorator(csrf_exempt)
def call_return_order(request):
    is_weixin = get_weixin_zhifubao(request)
    openid = get_open_id(request, is_weixin)
    trade_no = request.POST.get('trade_no')
    out_trade_no = request.POST.get('out_trade_no')

    update_lendhistorystatus(openid, 2)

    save_order(openid, out_trade_no, trade_no)

    return HttpResponse('success')


def contract(request):
    template_name = 'weixin/contract.html'
    response = render(request, template_name)
    return response


def about(request):
    template_name = 'weixin/about.html'
    response = render(request, template_name)
    return response


def privatecenter(request):
    template_name = 'weixin/privatecenter.html'

    set_weixin_zhifubao(request)
    is_weixin = get_weixin_zhifubao(request)

    openid = get_open_id(request, is_weixin)

    lendtime = get_lendtime(openid)

    deposit = float(get_deposit(openid, is_weixin))

    if is_weixin:
        user = get_user_info(openid)
        headimgurl = user['headimgurl']
        nick_name = user['nickname']
        subscribe_time = user['subscribe_time']

    else:
        headimgurl = request.session.get('avatar', default=None)
        nick_name = request.session.get('nick_name', default=None)

        if not headimgurl:
            headimgurl = ''
            nick_name = '亲爱的，轻拍用户'
        subscribe_time = get_subscribe_time(openid)

    context = {
        'lendtime': lendtime,
        'deposit': deposit,
        'headimgurl': headimgurl,
        'nickname': nick_name,
        'subscribe_time': subscribe_time,
        'is_weixin': is_weixin
    }
    response = render(request, template_name, context)
    return response


def wxconfig(request):
    mysql = MySQL()
    jsapi_ticket = mysql.get_jsapi_ticket()

    url = request.POST['url']

    timestamp = create_timestamp()
    noncestr = create_nonce_str()

    signature = get_signature(noncestr, jsapi_ticket, timestamp, url)

    ret_dict = {
        'appid': WEIXIN_APPID,
        'noncestr': noncestr,
        'timestamp': timestamp,
        'url': url,
        'signature': signature,
    }

    return JsonResponse(ret_dict)


@csrf_exempt
def wx(request):
    if request.method == 'GET':
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echostr = request.GET.get('echostr', '')
        try:
            check_signature(WECHAT_TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            echostr = 'error'
        return HttpResponse(echostr, content_type="text/plain")
    if request.method == 'POST':
        msg = parse_message(request.body)
        if msg.type == 'text':
            reply = create_reply('这是条文字消息', msg)
        elif msg.type == 'image':
            reply = create_reply('这是条图片消息', msg)
        elif msg.type == 'voice':
            reply = create_reply('这是条语音消息', msg)
        elif msg.type == 'event':
            subcribe_event = SubscribeEvent(msg)
            location_event = LocationEvent(msg)
            if msg.event == subcribe_event.event:
                reply = create_reply('欢迎您关注轻拍科技公众号', msg)
                openid = msg.source
                subcribe_save_openid(openid)
            elif msg.event == location_event.event:
                data = dict(xmltodict.parse(request.body)['xml'])
                try:
                    print('data', data)
                    lat = data['Latitude']
                    lon = data['Longitude']
                    request.session['lat'] = lat
                    request.session['lon'] = lon
                except:
                    request.session['lat'] = None
                    request.session['lon'] = None

                return 'success'
            else:
                return 'success'
        else:
            return 'success'
        response = HttpResponse(reply.render(), content_type="application/xml")

        return response
    else:
        print('error')


def oauth_user(request):
    from wechatpy import WeChatClient
    from wechatpy.oauth import WeChatOAuth

    # oauth = WeChatOAuth(WEIXIN_APPID, WEIXIN_APPSECRET, redirect_uri='http://relalive.com/weixin/lend/')

    oauth_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxe2d133d46896991&redirect_uri=http%3A%2F%2Frelalive.com%2Fweixin%2Flend%2F&response_type=code&scope=snsapi_userinfo&state=123&connect_redirect=1#wechat_redirect'

    req = urllib.request.Request(oauth_url)
    req.add_header('Content-Type', 'application/json')
    res = urllib.request.urlopen(req)


def set_weixin_zhifubao(request):

    code = request.GET.get('code', None)
    if code:
        if request.session.get('is_weixin', None) is None:
            request.session['is_weixin'] = True
    else:
        if request.session.get('is_weixin', None) is None:
            request.session['is_weixin'] = False


def get_weixin_zhifubao(request):
    return request.session.get('is_weixin', default=None)


def get_open_id(request, is_weixin):
    if is_weixin:
        code = request.GET.get('code', None)
    else:
        code = request.GET.get('auth_code', None)

    if code and not request.session.get('openid', default=None):
        openid = get_openid(code, is_weixin)
        request.session['openid'] = openid
    else:
        openid = request.session.get('openid', default=None)

    return openid












