from django.urls import path

from . import views

urlpatterns = [
    path("", views.menu, name="menu"),
    path("settings", views.settings, name="settings"),
    path("statistics", views.statistics, name="statistics"),
    path("training_session", views.training_session, name="training_session"),
    path("training_session/translate", views.translate, name="translate"),
    path("training_session/sound", views.sound, name="sound"),
    path("training_session/chatbot", views.chatbot, name="chatbot"),
]