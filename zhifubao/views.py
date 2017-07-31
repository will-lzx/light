import json

import alipay as alipay
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
    if request.method == 'GET':
        data = request.form.to_dict()
        signature = data.pop("sign")

        print(json.dumps(data))
        print(signature)

        # verify
        success = alipay.Alipay.verify_notify(request.GET['alipay'])
        if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            print("trade succeed")
    if request.method == 'POST':
        data = request.form.to_dict()
        signature = data.pop("sign")

        print(json.dumps(data))
        print(signature)

        # verify
        success = alipay.Alipay.verify_notify(request.GET['alipay'])
        if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            print("trade succeed")
