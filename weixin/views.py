from django.shortcuts import render

# Create your views here.


def weixin(request):
    template_name = 'weixin/home.html'
    response = render(request, template_name)
    return response
