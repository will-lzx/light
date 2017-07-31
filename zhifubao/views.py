import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt


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
    # if request.method == 'GET':
    #     signature = request.GET.get('signature', '')
    #     timestamp = request.GET.get('timestamp', '')
    #     nonce = request.GET.get('nonce', '')
    #     echostr = request.GET.get('echostr', '')
    #     try:
    #         check_signature(WECHAT_TOKEN, signature, timestamp, nonce)
    #     except InvalidSignatureException:
    #         echostr = 'error'
    #     return HttpResponse(echostr, content_type="text/plain")
    if request.method == 'POST':
        msg = request.body
        print(msg)
        return 'success'
    else:
        print('error')
