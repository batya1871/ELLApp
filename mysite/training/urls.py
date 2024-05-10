from django.urls import path

from . import views
app_name = "training"
urlpatterns = [
    path("", views.menu, name="menu"),
    path("settings", views.settings, name="settings"),
    path("statistic", views.statistic, name="statistic"),
    path("training_session", views.training_session, name="training_session"),
    path("training_session/<str:training_mode>/<str:difficulty_level>/", views.display_test, name="display_test"),
    path("training_session/<str:training_mode>/<str:difficulty_level>/<int:exercise_num>", views.display_exercise,
         name="display_exercise"),
    path('training_session/<str:training_mode>/<str:difficulty_level>/<int:exercise_num>/grade/',
         views.exercise_grade, name='exercise_grade'),
    path('training_session/<str:training_mode>/<str:difficulty_level>/results', views.results,
         name='results'),

    path("training_session/sound", views.sound, name="sound"),
    path("training_session/chatbot", views.chatbot, name="chatbot"),
]