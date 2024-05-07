from django.db import models


class User(models.Model):
    username = models.CharField("Логин", max_length=30)
    email = models.CharField("Эл. почта", max_lenght=100)
    password = models.CharField("Пароль", max_length=30)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Settings(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE())
    settings = models.TextField("Настройки")

    def __str__(self):
        return self.settings

    class Meta:
        verbose_name = "Настройки"
        verbose_name_plural = "Настройки"


class Grades(models.Model):
    grade = models.PositiveSmallIntegerField("Оценка")

    def __str__(self):
        return self.grade

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"


class Statistic(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE())
    translation_grades = models.ForeignKey(Grades, verbose_name="Оценки по переводу", on_delete=models.CASCADE())
    sound_grades = models.ForeignKey(Grades, verbose_name="Оценки по звучанию", on_delete=models.CASCADE())

    def calc_average_grade(self):
        return 4

    def __str__(self):
        return self.calc_average_grade()

    class Meta:
        verbose_name = "Статистика"
        verbose_name_plural = "Статистики"


class Exercise(models):
    task = models.TextField("Задание")
    correct_answer = models.TextField("Правильный ответ")

    def __str__(self):
        return self.task

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"


class Difficulty_level(models):
    name = models.CharField("Сложность", max_length=10)
    exercise = models.ForeignKey(Exercise, verbose_name="Задание", on_delete=models.CASCADE())

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Уровень сложности"
        verbose_name_plural = "Уровни сложности"


class Training_mode(models):
    name = models.CharField("Название", max_length=10)
    difficulty_level = models.ForeignKey(Difficulty_level, verbose_name="Уровень сложности", on_delete=models.CASCADE())

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Режим обучения"
        verbose_name_plural = "Режимы обучения"


class Training_session(models):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE())
    training_session = models.ForeignKey(Training_mode, verbose_name="Режим обучения", on_delete=models.CASCADE())

    def __str__(self):
        return self.user + "`s training session"

    class Meta:
        verbose_name = "Режим обучения"
        verbose_name_plural = "Режимы обучения"
