from django.http import HttpResponse
from .models import Statistic
from django.shortcuts import render

common_menu = [
    {'title': "Меню", 'url_name': 'training:menu'},
    {'title': "Войти", 'url_name': 'training:login'}
]
menu_list = [
    {'ref': 'training:training_session', 'content': 'Перейти к выбору режима'},
    {'ref': 'training:settings', 'content': 'Перейти к настройкам'},
    {'ref': 'training:statistic', 'content': 'Перейти к статистике'}
]
session_list = [
    {'ref': 'training:translate', 'content': 'Режим "перевод"'},
    {'ref': 'training:sound', 'content': 'Режим "звучание"'},
    {'ref': 'training:chatbot', 'content': 'Режим "чатбот"'}
]


def menu(request):
    data = {
        'title': "Меню",
        'menu_list': menu_list,
        'common_menu': common_menu
    }
    return render(request, "training/menu.html", context=data)


def settings(request):
    data = {
        'title': "Настройки",
        'common_menu': common_menu
    }
    return render(request, "training/settings.html", context=data)


def statistic(request):
    average_mark = Statistic.objects.get(pk=1).calc_average_grade()
    data = {'title': 'Статистика пользователя',
            "average_mark": average_mark,
            'common_menu': common_menu}
    return render(request, "training/statistic.html", context=data)


def training_session(request):
    data = {
        'title': "Выбор режима",
        'session_list': session_list,
        'common_menu': common_menu
    }
    return render(request, "training/training_session.html", context=data)


def translate(request):
    data = {
        'title': 'Режим "Перевод"',
        'common_menu': common_menu
    }
    return render(request, "training/translate.html", context=data)


def sound(request):
    data = {
        'title': 'Режим "Звучание"',
        'common_menu': common_menu
    }
    return render(request, "training/sound.html", context=data)


def chatbot(request):
    data = {
        'title': 'Режим "Чатбот"',
        'common_menu': common_menu
    }
    return render(request, "training/chatbot.html", context=data)


def login(request):
    return HttpResponse("Авторизация")
