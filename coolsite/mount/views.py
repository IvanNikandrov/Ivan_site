from django.shortcuts import render, HttpResponse,redirect
from django.http import HttpResponseNotFound



def index(request):
    return HttpResponse('Страница приложения mount.')


def archive(request, year):
    if int(year) > 2000:
        return redirect('home', permanent=True)


def categories(request, cat):
    if request.GET:
        print(request.GET)
    return HttpResponse(f'Страница номер: {cat}')




def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1> Страница не найдена </h1>')
