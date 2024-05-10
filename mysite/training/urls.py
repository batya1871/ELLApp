from django.urls import path

from . import views
app_name = "training"
urlpatterns = [
    path("", views.menu, name="menu"),
    path("settings", views.settings, name="settings"),
    path("statistic", views.statistic, name="statistic"),
    path("training_session", views.training_session, name="training_session"),
    path("training_session/translate/<str:difficulty_level>/", views.translate_display_test, name="translate_display_test"),
    path("training_session/translate/<str:difficulty_level>/<int:exercise_id>", views.translate_display_exercise,
         name="translate_display_exercise"),
    path('training_session/translate/<str:difficulty_level>/<int:exercise_id>/grade/',
         views.translate_exercise_grade, name='translate_exercise_grade'),
    path('training_session/translate/<str:difficulty_level>/results', views.translate_results,
         name='translate_results'),

    path("training_session/sound", views.sound, name="sound"),
    path("training_session/chatbot", views.chatbot, name="chatbot"),
]