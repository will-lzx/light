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
    url(r'^lendhistory/$', lendhistory, name='lendhistory'),

    url(r'^pay/$', PayView.as_view(), name='pay'),
    url(r'^call_save_order/$', call_save_order, name='call_save_order'),

    url(r'^privatecenter/$', privatecenter, name='privatecenter'),

    url(r'^withdraw/$', withdraw, name='withdraw'),
    url(r'^exe_withdraw/$', exe_withdraw, name='exe_withdraw'),

    # use help
    url(r'^use_help/$', use_help, name='use_help'),
    url(r'^use_help/deposit_question/$', deposit_question, name='deposit_question'),
    url(r'^use_help/get_fail/$', get_fail, name='get_fail'),
    url(r'^use_help/how_return/$', how_return, name='how_return'),
    url(r'^use_help/how_use/$', how_use, name='how_use'),
    url(r'^use_help/lost/$', lost, name='lost'),
    url(r'^use_help/several/$', several, name='several'),
    url(r'^use_help/how_pic/$', how_pic, name='how_pic'),
    url(r'^use_help/how_charge/$', how_charge, name='how_charge'),
    url(r'^about/$', about, name='about'),

    url(r'^return_pay/$', ReturnPayView.as_view(), name='return_pay'),
    url(r'^call_return_order/$', call_return_order, name='call_return_order'),

    url(r'^buy_tip/(?P<lendhistory_id>.+)/$', buy_tip, name='buy_tip'),

]
