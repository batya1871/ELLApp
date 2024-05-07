from django.db import models


class User(models.Model):
    username = models.CharField("Логин", max_length=30)
    email = models.CharField("Эл. почта", max_length=100)
    password = models.CharField("Пароль", max_length=30)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Settings(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
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
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    translation_grades = models.ManyToManyField(Grades, verbose_name="Оценки по переводу", related_name="translation_grades")
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


class Training_session(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

    def __str__(self):
        return self.user + "`s training session"

    class Meta:
        verbose_name = "Обучающая сессия"
        verbose_name_plural = "Обучающие сессии"


class Training_mode(models.Model):
    name = models.CharField("Название", max_length=10)
    training_session = models.ForeignKey(Training_session, verbose_name="Обучающая сессия", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Режим обучения"
        verbose_name_plural = "Режимы обучения"


class Difficulty_level(models.Model):
    name = models.CharField("Сложность", max_length=10)
    training_mode = models.ForeignKey(Training_mode, verbose_name="Режим обучения", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Уровень сложности"
        verbose_name_plural = "Уровни сложности"


class Exercise(models.Model):
    task = models.TextField("Задание")
    correct_answer = models.TextField("Правильный ответ")
    difficulty_level = models.ForeignKey(Difficulty_level, verbose_name="Уровень сложности", on_delete=models.CASCADE)

    def __str__(self):
        return self.task

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"
