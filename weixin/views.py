import hashlib
from io import BytesIO

import xmltodict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import smart_str
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from lxml import etree
from requests import session
from wechatpy.events import SubscribeEvent
from wechatpy.pay.api import WeChatRefund

from lib.utils import check_code
from lib.weixin.weixin_sql import *

from lib.utils.common import *
from wechatpy import parse_message, create_reply, WeChatPay
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException

from lib.utils.url_request import *
from weixin.api import Pay as PayApi


# Create your views here.

_letter_cases = "abcdefghjkmnpqrstuvwxy"
_upper_cases = _letter_cases.upper()
_numbers = ''.join(map(str, range(3, 10)))
init_chars = ''.join((_letter_cases, _upper_cases, _numbers))


@csrf_exempt
def weixin(request):
    if request.method == 'GET':
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)

        # 这里的token需要自己设定，主要是和微信的服务器完成验证使用
        token = WECHAT_TOKEN

        # 把token，timestamp, nonce放在一个序列中，并且按字符排序
        hashlist = [token, str(timestamp), str(nonce)]
        hashlist.sort()

        # 将上面的序列合成一个字符串
        hashstr = ''.join([s for s in hashlist])

        # 通过python标准库中的sha1加密算法，处理上面的字符串，形成新的字符串。
        hashstr = hashlib.sha1(hashstr.encode(encoding='utf-8')).hexdigest()

        # 把我们生成的字符串和微信服务器发送过来的字符串比较，
        # 如果相同，就把服务器发过来的echostr字符串返回去
        if hashstr == signature:
            return HttpResponse(echostr)

    if request.method == 'POST':
        # 将程序中字符输出到非 Unicode 环境（比如 HTTP 协议数据）时可以使用 smart_str 方法
        data = smart_str(request.body)
        # 将接收到数据字符串转成xml
        xml = etree.fromstring(data)

        # 从xml中读取我们需要的数据。注意这里使用了from接收的to，使用to接收了from，
        # 这是因为一会我们还要用这些数据来返回消息，这样一会使用看起来更符合逻辑关系
        fromUser = xml.find('ToUserName').text
        toUser = xml.find('FromUserName').text
        content = xml.find('Content').text

        # 这里获取当前时间的秒数，time.time()取得的数字是浮点数，所以有了下面的操作
        nowtime = str(int(time.time()))

        # 加载text.xml模板,参见render()调用render_to_string()并将结果馈送到 HttpResponse适合从视图返回的快捷方式 。
        rendered = render_to_string('weixin/text.xml',
                                    {'toUser': toUser, 'fromUser': fromUser, 'nowtime': nowtime, 'content': '微信功能正在开发中...'})
        return HttpResponse(rendered)


def create_code_img(request):
    # 直接在内存开辟一点空间存放临时生成的图片
    f = BytesIO()
    # 调用check_code生成照片和验证码
    img, code = check_code.create_validate_code()
    # 将验证码存在服务器的session中，用于校验
    request.session['check_code'] = code
    # 生成的图片放置于开辟的内存中
    img.save(f, 'PNG')
    # 将内存的数据读取出来，并以HttpResponse返回
    return HttpResponse(f.getvalue())


# def login(request):
#     template_name = 'weixin/login.html'
#     response = render(request, template_name)
#     return response


def agreement(request):
    template_name = 'weixin/agreement.html'
    response = render(request, template_name)
    return response


def lend(request):
    template_name = 'weixin/lend.html'

    code = request.GET.get('code', None)

    if code and not request.session.get('openid', default=None):
        print('code', code)
        openid = get_openid(code)
        request.session['openid'] = openid
    else:
        openid = request.session.get('openid', default=None)

    is_deposit = is_deposit_exist(openid)
    is_lend = is_lend_exist(openid)

    context = {
        'is_deposit': is_deposit,
        'openid': openid,
        'is_lend': is_lend
    }
    response = render(request, template_name, context)
    return response


def return_back(request):
    template_name = 'weixin/return.html'

    code = request.GET.get('code', None)

    if code and not request.session.get('openid', default=None):
        openid = get_openid(code)
        request.session['openid'] = openid
        request.GET.__delitem__('code')
    else:
        openid = request.session.get('openid', default=None)

    is_lend = is_lend_exist(openid)
    context = {
        'openid': openid,
        'is_lend': is_lend
    }

    response = render(request, template_name, context)
    return response


def output_tip(request):
    template_name = 'weixin/output_tip.html'
    has_opacity = False

    context = {
        'has_opacity': has_opacity
    }
    response = render(request, template_name, context)
    return response


def nearby(request):
    template_name = 'weixin/nearby.html'
    response = render(request, template_name)
    return response


def lendhistory(request):
    template_name = 'weixin/lendhistory.html'
    response = render(request, template_name)
    return response


def withdraw(request):
    template_name = 'weixin/withdraw.html'
    openid = request.session.get('openid', default=None)
    deposit = get_deposit(openid)
    deposit_order_id = get_order_id(openid)
    context = {
        'deposit': deposit,
        'deposit_order_id': deposit_order_id,
    }
    response = render(request, template_name, context)
    return response


@method_decorator(csrf_exempt)
def exe_withdraw(request):
    deposit = str(int(float(request.POST.get('deposit')) * 100))
    deposit_order_id = request.POST.get('deposit_order_id')
    openid = request.session.get('openid', default=None)
    refund_no = str(create_timestamp())
    wechatPay = WeChatPay(WEIXIN_APPID,
                          WECHAT[0]['key'],
                          WECHAT[0]['mch_id'],
                          mch_cert='/root/cert/apiclient_cert.pem',
                          mch_key='/root/cert/apiclient_key.pem')

    refund = WeChatRefund(wechatPay)

    resp = refund.apply(deposit, deposit, out_trade_no=deposit_order_id, out_refund_no=refund_no, op_user_id=WECHAT[0]['mch_id'])
    if resp['return_code'] == 'SUCCESS':
        update_deposit(openid, 0, 0)
    return HttpResponse(resp['return_code'])


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
        try:
            price = WEIXIN_DEPOSIT
            notify_url = WEIXIN_PAYBACK
            redirect_url = '/weixin/lend/'
            openid = request.GET['openid']
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
            'redirect_uri': redirect_url,
            'deposit': price,
        }
        return render(request, 'weixin/pay.html', data)


class WxPayNotifyView(View):
    """
    Receive wechat service data
    valid and send order_id, pay_number to notify_url
    """
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(WxPayNotifyView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pay = PayApi()
        data = request.body
        data = dict(xmltodict.parse(data)['xml'])
        result = {}
        sign = data['sign']
        del data['sign']
        if sign:
            price = WEIXIN_DEPOSIT
            total_fee = price
            openid = data['openid']
            order_id = data['out_trade_no']
            pay_number = data['transaction_id']
            update_deposit(openid, total_fee, order_id)
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

    code = request.GET.get('code', None)

    if code and not request.session.get('openid', default=None):
        print('code', code)
        openid = get_openid(code)
        request.session['openid'] = openid
    else:
        openid = request.session.get('openid', default=None)

    lendtime = get_lendtime(openid)

    deposit = float(get_deposit(openid))

    user = get_user_info(openid)

    context = {
        'lendtime': lendtime,
        'deposit': deposit,
        'headimgurl': user['headimgurl'],
        'nickname': user['nickname'],
        'subscribe_time': user['subscribe_time'],
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
            if msg.event == subcribe_event.event:
                reply = create_reply('欢迎您关注轻拍科技公众号', msg)
                openid = msg.source
                subcribe_save_openid(openid)
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











