# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.


def home(request):
    template_name = 'home/home.html'
    respone = render(request, template_name)
    return respone