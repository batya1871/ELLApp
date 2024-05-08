from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Statistic
from django.shortcuts import render

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

@login_required
def menu(request):
    data = {
        'title': "Меню",
        'menu_list': menu_list,
    }
    return render(request, "training/menu.html", context=data)

@login_required
def settings(request):
    data = {
        'title': "Настройки",
    }
    return render(request, "training/settings.html", context=data)

@login_required
def statistic(request):
    average_mark = Statistic.objects.get(pk=1).calc_average_grade()
    data = {'title': 'Статистика пользователя',
            "average_mark": average_mark,}
    return render(request, "training/statistic.html", context=data)

@login_required
def training_session(request):
    data = {
        'title': "Выбор режима",
        'session_list': session_list,
    }
    return render(request, "training/training_session.html", context=data)

@login_required
def translate(request):
    data = {
        'title': 'Режим "Перевод"',
    }
    return render(request, "training/translate.html", context=data)

@login_required
def sound(request):
    data = {
        'title': 'Режим "Звучание"',
    }
    return render(request, "training/sound.html", context=data)

@login_required
def chatbot(request):
    data = {
        'title': 'Режим "Чатбот"',
    }
    return render(request, "training/chatbot.html", context=data)

