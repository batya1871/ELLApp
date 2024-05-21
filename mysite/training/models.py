from random import randint

from django.contrib.auth.models import AbstractUser
from django.db import models


class Student(AbstractUser):
    statistic = models.OneToOneField('Statistic', on_delete=models.SET_NULL, null=True, blank=True, related_name="user")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def clean_data(self):
        self.choice_set.all().delete()
        self.result_set.all().delete()

    def is_answered_check(self, check_exercise):
        check = self.choice_set.filter(exercise=check_exercise)
        return check.first().user_answer if check.count() > 0 else None

    def get_skipped_exercise_count(self, exercises):
        return len(exercises) - self.choice_set.count()

    def get_answer_if_choice_wrong(self, exercise):
        choice = self.choice_set.filter(exercise=exercise)
        correct_answers = exercise.get_correct_answers().values_list('answer', flat=True)
        correct_answers = [answer.lower() for answer in correct_answers]
        if choice.first().user_answer.lower() not in correct_answers:
            return choice.first().user_answer
        return None

    def create_statistic(self):
        statistic = Statistic.objects.create()
        statistic.save()
        self.statistic = statistic
        self.save()


class Grades(models.Model):
    grade = models.PositiveSmallIntegerField("Оценка")

    def __str__(self):
        return str(self.grade)

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"


class Statistic(models.Model):
    translate_grades = models.ManyToManyField(Grades, verbose_name="Оценки по переводу",
                                              related_name="translation_grades")
    sound_grades = models.ManyToManyField(Grades, verbose_name="Оценки по звучанию", related_name="sound_grades")

    def calc_average_grade(self):
        grades = 0
        for sound_grade in self.sound_grades.all():
            grades += sound_grade.grade
        for translate_grade in self.translate_grades.all():
            grades += translate_grade.grade
        common_count = (self.sound_grades.count() + self.translate_grades.count())
        return grades / common_count if common_count > 0 else 0

    def calc_average_grade_by_sound(self):
        grades = 0
        for sound_grade in self.sound_grades.all():
            grades += sound_grade.grade
        return grades / self.sound_grades.count() if self.sound_grades.count() > 0 else 0

    def calc_average_grade_by_translate(self):
        grades = 0
        for translate_grades in self.translate_grades.all():
            grades += translate_grades.grade
        return grades / self.translate_grades.count() if self.translate_grades.count() > 0 else 0

    def add_grade(self, grade, training_mode):
        match training_mode:
            case "translate":
                self.translate_grades.create(grade=grade)
            case "sound":
                self.sound_grades.create(grade=grade)
        self.save()

    def __str__(self):
        return str(self.calc_average_grade())

    class Meta:
        verbose_name = "Статистика"
        verbose_name_plural = "Статистики"


class Training_mode(models.Model):
    name = models.CharField("Название", max_length=10, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Режим обучения"
        verbose_name_plural = "Режимы обучения"


class Difficulty_level(models.Model):
    name = models.CharField("Сложность", max_length=20, unique=True)
    training_mode = models.ForeignKey(Training_mode, verbose_name="Режим обучения", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Уровень сложности"
        verbose_name_plural = "Уровни сложности"

    def get_first_exercise_block(self):
        return self.exercise_block_set.first()

    def deactivate_all_blocks(self):
        for ex_block in self.exercise_block_set.all():
            ex_block.active_off()

    def get_random_exercise_block(self):
        ex_block = self.exercise_block_set.all()[randint(0, self.exercise_block_set.count() - 1)]
        ex_block.active_on()
        return ex_block


class Exercise_block(models.Model):
    name = models.TextField("Название теста", unique=True)
    difficulty_level = models.ForeignKey(Difficulty_level, verbose_name="Уровень сложности", on_delete=models.CASCADE)
    is_active_block = models.BooleanField("Активный блок", default=False)

    def set_nums(self):
        exercises = self.exercise_set.all()
        for ind, exercise in enumerate(exercises):
            exercise.num = ind
            exercise.save()

    def active_on(self):
        self.is_active_block = True
        self.save()

    def active_off(self):
        self.is_active_block = False
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"


class Exercise(models.Model):
    task = models.TextField("Задание", blank=True)
    num = models.IntegerField("Номер в списке", default=0)
    exercise_block = models.ForeignKey(Exercise_block, verbose_name="Тест", on_delete=models.CASCADE)
    audio_task = models.FileField(upload_to="sound", default=None,
                                  null=True, verbose_name="Аудио-задание")

    def __str__(self):
        return "№" + str(self.num) + " Задание: " + str(self.task)

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

    def get_correct_answers(self):
        return self.correct_answers_set.all()


class Correct_Answers(models.Model):
    exercise = models.ForeignKey(Exercise, verbose_name="Задание", on_delete=models.CASCADE)
    answer = models.TextField("Правильный ответ")

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class Choice(models.Model):
    user = models.ForeignKey(Student, verbose_name="Пользователь", on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, verbose_name="Задание", on_delete=models.CASCADE)
    user_answer = models.TextField("Ответ пользователя")


class Result(models.Model):
    training_mode = models.ForeignKey(Training_mode, verbose_name="Режим обучения", on_delete=models.CASCADE)
    user = models.ForeignKey(Student, verbose_name="Пользователь", on_delete=models.CASCADE)
    correct = models.IntegerField("Кол-во правильных ответов", default=0)
    wrong = models.IntegerField("Кол-во неправильных ответов", default=0)
    processed = models.BooleanField("Это поле обработано", default=False)

    def end_of_processing(self):
        self.processed = True
        self.save()
