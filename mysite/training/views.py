from itertools import chain
from operator import attrgetter

from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpResponse
from django.urls import reverse_lazy

from .models import Statistic, Difficulty_level, Exercise, Choice, Result, Training_mode
from django.shortcuts import render, redirect, get_object_or_404

menu_list = [
    {'ref': 'training:training_session', 'content': 'Перейти к выбору режима'},
    {'ref': 'training:settings', 'content': 'Перейти к настройкам'},
    {'ref': 'training:statistic', 'content': 'Перейти к статистике'}
]
session_list = [
    {'ref': 'training:sound', 'content': 'Режим "звучание"'},
    {'ref': 'training:chatbot', 'content': 'Режим "чатбот"'}
]

value_diff_list = {
    '1': 'easy-translate',
    '2': 'medium-translate',
    '3': 'hard-translate'
}


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
            "average_mark": average_mark, }
    return render(request, "training/statistic.html", context=data)


@login_required
def training_session(request):
    if request.method == "POST":
        typeOfTraining = request.POST['TypeOfTraining']
        if typeOfTraining == "Translate":
            difficulty_level = value_diff_list[request.POST['diff_option']]
            return redirect(reverse_lazy('training:translate_display_test',
                                         kwargs={'difficulty_level': difficulty_level}))
    data = {
        'title': "Выбор режима",
        'session_list': session_list,
    }
    return render(request, "training/training_session.html", context=data)


@login_required
def translate_display_test(request, difficulty_level):
    request.user.clean_data()
    difficulty_level_bd = get_object_or_404(Difficulty_level, name=difficulty_level)
    exercise_block = difficulty_level_bd.exercise_block_set.first()
    exercise_block.set_nums()
    return redirect(reverse_lazy('training:translate_display_exercise',
                                 kwargs={'difficulty_level': difficulty_level,
                                         'exercise_id': 0}))


@login_required
def translate_display_exercise(request, difficulty_level, exercise_id):
    difficulty_level_bd = get_object_or_404(Difficulty_level, name=difficulty_level)
    exercise_block = difficulty_level_bd.exercise_block_set.first()
    exercises = exercise_block.exercise_set.all()
    current_exercise, next_exercise, prev_exercise = None, None, None
    current_exercise = exercises[exercise_id]
    if exercise_id != len(exercises) - 1:
        next_exercise = exercises[exercise_id + 1]
    if exercise_id != 0:
        prev_exercise = exercises[exercise_id - 1]

    users_answer = request.user.is_answered_check(current_exercise)
    context = {'difficulty_level': difficulty_level,
               'exercise': current_exercise,
               'next_exercise': next_exercise,
               'prev_exercise': prev_exercise,
               'users_answer': users_answer,
               'title': "Вопрос №" + str(exercise_id + 1)}
    return render(request,
                  'training/translate_display_exercise.html', context)


@login_required
def translate_exercise_grade(request, difficulty_level, exercise_id):
    difficulty_level_bd = get_object_or_404(Difficulty_level, name=difficulty_level)
    exercise_block = difficulty_level_bd.exercise_block_set.first()
    exercises = exercise_block.exercise_set.all()
    exercise = exercises[exercise_id]
    if not request.user.is_answered_check(exercise) and request.method == "POST":
        correct_answers = exercise.get_correct_answers().values_list('answer', flat=True)
        user_answer = request.POST['answer']
        user_answer = " ".join(user_answer.split())
        choice = Choice(user=request.user,
                        exercise=exercise, user_answer=user_answer)
        choice.save()
        correct_answers = [answer.lower() for answer in correct_answers]

        is_correct = user_answer.lower() in correct_answers
        result, created = Result.objects.get_or_create(user=request.user,
                                                       training_mode=(get_object_or_404(Training_mode, name="Перевод")))
        if is_correct is True:
            result.correct = F('correct') + 1
        else:
            result.wrong = F('wrong') + 1
        result.save()

    if exercise_id != len(exercises) - 1:
        return redirect(reverse_lazy('training:translate_display_exercise',
                                     kwargs={'difficulty_level': difficulty_level,
                                             'exercise_id': exercise_id + 1}))
    else:

        skipped_exercises_count = request.user.get_skipped_exercise_count(exercises)
        context = {'difficulty_level': difficulty_level,
                   'first_exercise_id': 0,
                   'skipped_exercises_count': skipped_exercises_count,
                   'title': "Переход к результатам"}
        return render(request,
                      'training/translate_before_result.html', context)


@login_required
def translate_results(request, difficulty_level):
    difficulty_level_bd = get_object_or_404(Difficulty_level, name=difficulty_level)
    exercise_block = difficulty_level_bd.exercise_block_set.first()
    exercises = exercise_block.exercise_set.all()
    results = Result.objects.filter(user=request.user,
                                    training_mode=(get_object_or_404(Training_mode, name="Перевод"))).values()
    correct = [i['correct'] for i in results][0] if len([i['correct'] for i in results]) > 0 else 0
    wrong = [i['wrong'] for i in results][0] if len([i['wrong'] for i in results]) > 0 else 0
    skipped = len(exercises) - (correct + wrong) if len(exercises) - (correct + wrong) > 0 else 0
    for exercise in exercises:
        if request.user.is_answered_check(exercise) is None:
            choice = Choice(user=request.user,
                            exercise=exercise, user_answer="")
            choice.save()
    wrong_answers = []
    wrong_exercises = []
    correct_answers = []
    for exercise in exercises:
        if request.user.get_answer_if_choice_wrong(exercise) is not None:
            wrong_answers.append(request.user.get_answer_if_choice_wrong(exercise))
            wrong_exercises.append(exercise)
            correct_answers.append(exercise.get_correct_answers().first())
    wrong_data = [{'wrong_answers': t[0], 'wrong_exercises': t[1], 'correct_answers': t[2]} for t in zip(wrong_answers,
                                                                                                         wrong_exercises,
                                                                                                         correct_answers)]
    context = {'difficulty_level': difficulty_level,
               'correct': correct,
               'wrong': wrong,
               'number': len(exercises),
               'skipped': skipped,
               'title': "Результаты",
               'wrong_data': wrong_data}
    # request.user.clean_data()
    return render(request,
                  'training/translate_results.html', context)


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
