from django.contrib.auth.models import AbstractUser
from django.db import models


class Student(AbstractUser):

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


class Settings(models.Model):
    user = models.ForeignKey(Student, verbose_name="Пользователь", on_delete=models.CASCADE)
    settings = models.TextField("Настройки")

    def __str__(self):
        return self.settings

    class Meta:
        verbose_name = "Настройки"
        verbose_name_plural = "Настройки"


class Grades(models.Model):
    grade = models.PositiveSmallIntegerField("Оценка")

    def __str__(self):
        return str(self.grade)

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"


class Statistic(models.Model):
    user = models.ForeignKey(Student, verbose_name="Пользователь", on_delete=models.CASCADE)
    translation_grades = models.ManyToManyField(Grades, verbose_name="Оценки по переводу",
                                                related_name="translation_grades")
    sound_grades = models.ManyToManyField(Grades, verbose_name="Оценки по звучанию", related_name="sound_grades")

    def calc_average_grade(self):
        grades = 0
        for sound_grade in self.sound_grades.all():
            grades += sound_grade.grade
        for translation_grade in self.translation_grades.all():
            grades += translation_grade.grade
        return grades / (self.sound_grades.count() + self.translation_grades.count())

    def __str__(self):
        return str(self.calc_average_grade())

    class Meta:
        verbose_name = "Статистика"
        verbose_name_plural = "Статистики"


class Training_mode(models.Model):
    name = models.CharField("Название", max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Режим обучения"
        verbose_name_plural = "Режимы обучения"


class Difficulty_level(models.Model):
    name = models.CharField("Сложность", max_length=20)
    training_mode = models.ForeignKey(Training_mode, verbose_name="Режим обучения", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Уровень сложности"
        verbose_name_plural = "Уровни сложности"

    def get_first_exercise_block(self):
        return self.exercise_block_set.first()


class Exercise_block(models.Model):
    name = models.TextField("Название теста")
    difficulty_level = models.ForeignKey(Difficulty_level, verbose_name="Уровень сложности", on_delete=models.CASCADE)

    def set_nums(self):
        exercises = self.exercise_set.all()
        for ind, exercise in enumerate(exercises):
            exercise.num = ind
            exercise.save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"


class Exercise(models.Model):
    task = models.TextField("Задание", blank=True, default="Task in audio file")
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
