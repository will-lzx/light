from django.shortcuts import render
from django.http import HttpResponse
import hashlib
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
import time
from lxml import etree
from django.template.loader import render_to_string
from django.views.decorators.csrf import ensure_csrf_cookie
from light.settings import *
# Create your views here.


@csrf_exempt
@ensure_csrf_cookie
def weixin(request):
    if request.method == 'GET':
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)

        # 这里的token需要自己设定，主要是和微信的服务器完成验证使用
        token = WECHAT_TOKEN

        # 把token，timestamp, nonce放在一个序列中，并且按字符排序
        hashlist = [token, timestamp, nonce]
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
