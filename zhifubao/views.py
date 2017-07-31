import json

import alipay as alipay
import xmltodict
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
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
    if request.method == 'GET':
        alipay = request.registry['alipay']
        if alipay.verify_notify(**request.params):
            print(alipay)
        else:
            print('erroe')
    if request.method == 'POST':
        message = xmltodict.parse(to_text(request.body))['xml']

        if message.verify_notify(**request.params):
            print(message)
        else:
            print('erroe')
