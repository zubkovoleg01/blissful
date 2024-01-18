from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('Главная страница')

def post(request):
    return HttpResponse('Пост')

def post_detail(request, pk):
    return HttpResponse(f'{pk}')
