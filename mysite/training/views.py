from django.http import HttpResponse


def menu(request):
    return HttpResponse("This is main menu")


def settings(request):
    return HttpResponse("This is settings")


def statistics(request):
    return HttpResponse("This is statistics")


def training_session(request):
    return HttpResponse("This is training_session. You can choose training mode")


def translate(request):
    return HttpResponse("This is translate mode")


def sound(request):
    return HttpResponse("This is sound mode")


def chatbot(request):
    return HttpResponse("This is chatbot mode")
