from django.shortcuts import render

# Create your views here.


def home(request):
    template_name = 'home/home.html'
    response = render(request, template_name)
    return response


def ownpic(request):
    template_name = 'home/ownpic.html'
    response = render(request, template_name)
    return response


def about(request):
    template_name = 'home/about.html'
    response = render(request, template_name)
    return response