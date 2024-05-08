from django.urls import path

from . import views
app_name = "training"
urlpatterns = [
    path("", views.menu, name="menu"),
    path("settings", views.settings, name="settings"),
    path("statistic", views.statistic, name="statistic"),
    path("training_session", views.training_session, name="training_session"),
    path("training_session/translate", views.translate, name="translate"),
    path("training_session/sound", views.sound, name="sound"),
    path("training_session/chatbot", views.chatbot, name="chatbot"),
    path("login/", views.login, name="login"),
]