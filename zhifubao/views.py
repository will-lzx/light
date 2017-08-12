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
from django.views.decorators.csrf import csrf_exempt

from light.settings import *
import requests
from lib.utils.common import *


def lend(request):
    #user_id = get_user_id(request)
    # print('user_id:', user_id)
    template_name = 'zhifubao/lend.html'
    print('test:')
    response = render(request, template_name)
    print('response:', response)
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
        request.session['user_id'] = user_id
    else:
        user_id = request.session.get('user_id', default=None)

    return user_id













