from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    template = 'posts/index.html'
    text = 'Это главная страница проекта Blissful'
    context = {
        'text': text,
    }
    return render(request, template, context)

def group_list(request):
    template = 'posts/group_list.html'
    text = 'Здесь будет информация о группах проекта Blissful'
    context = {
        'text': text,
    }
    return render(request, template, context)

def post_detail(request, pk):
    return HttpResponse(f'{pk}')
