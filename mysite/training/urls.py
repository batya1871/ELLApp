from django.urls import path

from . import views
app_name = "training"
urlpatterns = [
    path("", views.training_session, name="training_session"),
    path("statistic", views.statistic, name="statistic"),

    path("training_session/<str:training_mode>/<str:difficulty_level>/", views.display_test, name="display_test"),
    path("training_session/<str:training_mode>/<str:difficulty_level>/<int:exercise_num>", views.display_exercise,
         name="display_exercise"),
    path('training_session/<str:training_mode>/<str:difficulty_level>/<int:exercise_num>/grade/',
         views.exercise_grade, name='exercise_grade'),
    path('training_session/<str:training_mode>/<str:difficulty_level>/results', views.results,
         name='results'),
]