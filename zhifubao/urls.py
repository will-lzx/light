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
from zhifubao.views import *

urlpatterns = [
    # url(r'^$', zhifubao, name='zhifubao'),
    url(r'^call_back/$', call_back, name='call_back'),

    url(r'^lend/$', lend, name='lend'),
    url(r'^return_back/$', return_back, name='return_back'),
    url(r'^return_tip/(?P<has_capacity>.+)/(?P<cabinet_code>.+)/$', return_tip, name='output_tip'),

    url(r'^nearby/$', nearby, name='nearby'),


    url(r'^output_tip/(?P<has_pole>.+)/(?P<cabinet_code>.+)/$', output_tip, name='output_tip'),
    url(r'^generate_lendhistory/$', generate_lendhistory, name='generate_lendhistory'),
    url(r'^update_lendhistory/$', update_lendhistory, name='update_lendhistory'),
    url(r'^get_pole/$', get_pole, name='get_pole'),

    url(r'^lend_success/$', lend_success, name='lend_success'),

    url(r'^pay/$', PayView.as_view(), name='pay'),
    url(r'^call_save_order/$', call_save_order, name='call_save_order'),

    url(r'^privatecenter/$', privatecenter, name='privatecenter'),

]
