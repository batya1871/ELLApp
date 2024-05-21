
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpResponse
from django.urls import reverse_lazy

from .models import Statistic, Difficulty_level, Choice, Result, Training_mode
from django.shortcuts import render, redirect, get_object_or_404

menu_list = [
    {'ref': 'training:training_session', 'content': 'Выбор режима'},
    {'ref': 'training:statistic', 'content': 'Статистика пользователя'},
    {'ref': 'training:settings', 'content': 'Настройки'}
]

value_diff_list = {
    '1': 'easy-translate',
    '2': 'medium-translate',
    '3': 'hard-translate',
    '4': 'easy-sound',
    '5': 'medium-sound',
    '6': 'hard-sound',
}


def get_grade(count, correct_count, difficulty_level):
    percentage = correct_count / count * 100
    grade_thresholds = {
        "easy": [(90, 5, "greate-grade"), (70, 4, "good-grade"), (50, 3, "ok-grade")],
        "medium": [(80, 5, "greate-grade"), (60, 4, "good-grade"), (40, 3, "ok-grade")],
        "hard": [(70, 5, "greate-grade"), (50, 4, "good-grade"), (30, 3, "ok-grade")]
    }

    for threshold, grade, grade_style in grade_thresholds[difficulty_level.split("-")[0]]:
        if percentage >= threshold:
            return grade, grade_style

    return 2, "bad-grade"


@login_required
def statistic(request):
    statistic_of_user = request.user.statistic
    statistic_exist = statistic_of_user is not None
    average_translate, average_sound, common_average, translate_count, sound_count, common_count = None, None, None, None, None, None
    if statistic_exist:
        average_translate = round(statistic_of_user.calc_average_grade_by_translate(), 2)
        average_sound = round(statistic_of_user.calc_average_grade_by_sound(), 2)
        common_average = round(statistic_of_user.calc_average_grade(), 2)
        translate_count = statistic_of_user.translate_grades.count()
        sound_count = statistic_of_user.sound_grades.count()
        common_count = sound_count + translate_count
    data = {'title': 'Статистика пользователя',
            'statistic_exist': statistic_exist,
            'average_translate': average_translate,
            'average_sound': average_sound,
            'common_average': common_average,
            'translate_count': translate_count,
            'sound_count': sound_count,
            'common_count': common_count,
            'menu_list': menu_list,
            }
    return render(request, "training/statistic.html", context=data)


@login_required
def training_session(request):
    if request.method == "POST":
        typeOfTraining = request.POST['TypeOfTraining']
        if typeOfTraining == "translate" or typeOfTraining == "sound":
            difficulty_level = value_diff_list[request.POST[f'diff_option_{typeOfTraining}']]
            return redirect(reverse_lazy('training:display_test',
                                         kwargs={'training_mode': typeOfTraining,
                                                 'difficulty_level': difficulty_level}))
    data = {
        'title': "Выбор режима",
        'menu_list': menu_list,
    }
    return render(request, "training/training_session.html", context=data)


@login_required
def display_test(request, training_mode, difficulty_level):
    request.user.clean_data()
    difficulty_level_bd = get_object_or_404(Difficulty_level, name=difficulty_level)
    difficulty_level_bd.deactivate_all_blocks()
    exercise_block = difficulty_level_bd.get_random_exercise_block()
    exercise_block.set_nums()
    if request.user.statistic is None:
        request.user.create_statistic()
    results_new = Result.objects.create(user=request.user,
                                        training_mode=(
                                            get_object_or_404(Training_mode, name=training_mode)))
    results_new.save()
    return redirect(reverse_lazy('training:display_exercise',
                                 kwargs={'training_mode': training_mode,
                                         'difficulty_level': difficulty_level,
                                         'exercise_num': 0}))


@login_required
def display_exercise(request, training_mode, difficulty_level, exercise_num):
    difficulty_level_bd = get_object_or_404(Difficulty_level, name=difficulty_level)
    exercise_block = difficulty_level_bd.exercise_block_set.filter(is_active_block=True)[0]
    exercises = exercise_block.exercise_set.order_by('num')
    current_exercise, next_exercise, prev_exercise = None, None, None
    current_exercise = exercises[exercise_num]
    if exercise_num != len(exercises) - 1:
        next_exercise = exercises[exercise_num + 1]
    if exercise_num != 0:
        prev_exercise = exercises[exercise_num - 1]

    users_answer = request.user.is_answered_check(current_exercise)

    context = {'training_mode': training_mode,
               'difficulty_level': difficulty_level,
               'exercise': current_exercise,
               'next_exercise': next_exercise,
               'prev_exercise': prev_exercise,
               'users_answer': users_answer,
               'title': "Вопрос №" + str(exercise_num + 1),
               'menu_list': menu_list,
               }
    return render(request,
                  'training/display_exercise.html', context)


@login_required
def exercise_grade(request, training_mode, difficulty_level, exercise_num):
    difficulty_level_bd = get_object_or_404(Difficulty_level, name=difficulty_level)
    exercise_block = difficulty_level_bd.exercise_block_set.filter(is_active_block=True)[0]
    exercises = exercise_block.exercise_set.order_by('num')
    exercise = exercises[exercise_num]
    if not request.user.is_answered_check(exercise) and request.method == "POST":
        correct_answers = exercise.get_correct_answers().values_list('answer', flat=True)
        user_answer = request.POST['answer']
        user_answer = " ".join(user_answer.split())
        choice = Choice(user=request.user,
                        exercise=exercise, user_answer=user_answer)
        choice.save()
        correct_answers = [answer.lower() for answer in correct_answers]

        is_correct = user_answer.lower() in correct_answers
        result = Result.objects.get(user=request.user,
                                    training_mode=(
                                        get_object_or_404(Training_mode, name=training_mode)))
        if is_correct is True:
            result.correct = F('correct') + 1
        else:
            result.wrong = F('wrong') + 1
        result.save()

    if exercise_num != len(exercises) - 1:
        return redirect(reverse_lazy('training:display_exercise',
                                     kwargs={'training_mode': training_mode,
                                             'difficulty_level': difficulty_level,
                                             'exercise_num': exercise_num + 1}))
    else:
        skipped_exercises_count = request.user.get_skipped_exercise_count(exercises)
        context = {'training_mode': training_mode,
                   'difficulty_level': difficulty_level,
                   'first_exercise_num': 0,
                   'skipped_exercises_count': skipped_exercises_count,
                   'title': "Переход к результатам",
                   'menu_list': menu_list}
        return render(request,
                      'training/before_result.html', context)


@login_required
def results(request, training_mode, difficulty_level):
    difficulty_level_bd = get_object_or_404(Difficulty_level, name=difficulty_level)
    exercise_block = difficulty_level_bd.exercise_block_set.filter(is_active_block=True)[0]
    exercise_block.active_off()
    exercises = exercise_block.exercise_set.order_by('num')
    results_of_test = Result.objects.filter(user=request.user,
                                            training_mode=(
                                                get_object_or_404(Training_mode, name=training_mode)))[0]

    correct, wrong, skipped = 0, 0, 10
    correct = results_of_test.correct if results_of_test.correct > 0 else 0
    wrong = results_of_test.wrong if results_of_test.wrong > 0 else 0
    skipped = len(exercises) - (correct + wrong)
    grade, grade_style = get_grade(len(exercises), correct, difficulty_level)
    if not results_of_test.processed:
        stat = request.user.statistic
        stat.add_grade(grade, training_mode)
        results_of_test.end_of_processing()
    result_data = {'correct': correct, 'wrong': wrong, 'skipped': skipped, 'number': len(exercises), 'grade': grade}
    for exercise in exercises:
        if request.user.is_answered_check(exercise) is None:
            choice = Choice(user=request.user,
                            exercise=exercise, user_answer="")
            choice.save()
    wrong_answers, wrong_exercises, correct_answers = [], [], []
    for exercise in exercises:
        if request.user.get_answer_if_choice_wrong(exercise) is not None:
            wrong_answers.append(request.user.get_answer_if_choice_wrong(exercise))
            wrong_exercises.append(exercise)
            correct_answers.append(exercise.get_correct_answers().first())
    wrong_data = [{'wrong_answers': t[0], 'wrong_exercises': t[1], 'correct_answers': t[2]} for t in zip(wrong_answers,
                                                                                                         wrong_exercises,
                                                                                                         correct_answers)]
    context = {'training_mode': training_mode,
               'difficulty_level': difficulty_level,
               'title': "Результаты",
               'result_data': result_data,
               'wrong_data': wrong_data,
               'menu_list': menu_list,
               'grade_style': grade_style}
    return render(request,
                  'training/results.html', context)
