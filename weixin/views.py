from django.shortcuts import render
from django.http import HttpResponse
import hashlib
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
import time

from io import BytesIO
from lxml import etree
from django.template.loader import render_to_string
from django.views.decorators.csrf import ensure_csrf_cookie
from light.settings import *
import random
from lib.utils import check_code
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


def checkSignature(request):
    signature=request.GET.get('signature', None)
    timestamp=request.GET.get('timestamp', None)
    nonce=request.GET.get('nonce', None)
    echostr=request.GET.get('echostr', None)
    #这里的token我放在setting，可以根据自己需求修改
    token = WECHAT_TOKEN

    tmplist=[token, timestamp, nonce]
    tmplist.sort()
    tmpstr="%s%s%s"%tuple(tmplist)
    tmpstr=hashlib.sha1(tmpstr).hexdigest()
    if tmpstr == signature:
        return echostr
    else:
        return None


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


def login(request):
    template_name = 'weixin/login.html'
    response = render(request, template_name)
    return response


def agreement(request):
    template_name = 'weixin/agreement.html'
    response = render(request, template_name)
    return response


def lend(request):
    template_name = 'weixin/lend.html'
    response = render(request, template_name)
    return response


def return_back(request):
    template_name = 'weixin/return.html'
    response = render(request, template_name)
    return response
