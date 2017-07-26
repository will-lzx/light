"""l URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from weixin.views import *

urlpatterns = [
    url(r'^$', weixin, name='weixin'),
    url(r'^create_code_img/', create_code_img, name='create_code_img'),
    url(r'^agreement/', agreement, name='agreement'),

    url(r'^lend/$', lend, name='lend'),
    url(r'^return_back/$', return_back, name='return_back'),
    url(r'^nearby/$', nearby, name='nearby'),

    url(r'^lendhistory/$', lendhistory, name='lendhistory'),
    url(r'^withdraw/$', withdraw, name='withdraw'),

    url(r'^use_help/$', use_help, name='use_help'),
    url(r'^about/$', about, name='about'),

    url(r'^privatecenter/$', privatecenter, name='privatecenter'),

    url(r'^wxconfig/$', wxconfig, name='wxconfig'),

    url(r'^wx/$', wx, name='wx'),

]
