import hashlib
from collections import OrderedDict

from django.core.serializers import json
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from alipay import AliPay


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
    alipay = AliPay(
        appid="2017072707914385",
        app_notify_url="http://relalive.com/zhifubao/alipy_notify/",
        app_private_key_path="",
        alipay_public_key_path="",
        sign_type="RSA2",
        debug=False
    )

    serializer = MySerialiser()
    data = serializer.serialize(request.body)

    success = alipay.verify(data, sign)

    if success:
        return 'success'
    else:
        return 'fail'


def alipy_notify(request):
    print('notify')


from django.core.serializers.python import Serializer


class MySerialiser(Serializer):
    def end_object( self, obj ):
        self._current['id'] = obj._get_pk_val()
        self.objects.append( self._current )



