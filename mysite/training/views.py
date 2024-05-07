from django.http import HttpResponse
from .models import Statistic
from django.shortcuts import render


def menu(request):
    return render(request, "training/menu.html")


def settings(request):
    return render(request, "training/settings.html")


def statistic(request):
    average_mark = Statistic.objects.get(pk=1).calc_average_grade()
    context = {"average_mark": average_mark}
    return render(request, "training/statistic.html", context)


def training_session(request):
    return render(request, "training/training_session.html")


def translate(request):
    return render(request, "training/translate.html")


def sound(request):
    return render(request, "training/sound.html")


def chatbot(request):
    return render(request, "training/chatbot.html")
