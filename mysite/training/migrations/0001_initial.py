# Generated by Django 5.0.5 on 2024-05-07 12:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Difficulty_level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='Сложность')),
            ],
            options={
                'verbose_name': 'Уровень сложности',
                'verbose_name_plural': 'Уровни сложности',
            },
        ),
        migrations.CreateModel(
            name='Grades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.PositiveSmallIntegerField(verbose_name='Оценка')),
            ],
            options={
                'verbose_name': 'Оценка',
                'verbose_name_plural': 'Оценки',
            },
        ),
        migrations.CreateModel(
            name='Training_mode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Режим обучения',
                'verbose_name_plural': 'Режимы обучения',
            },
        ),
        migrations.CreateModel(
            name='Training_session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Режим обучения',
                'verbose_name_plural': 'Режимы обучения',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, verbose_name='Логин')),
                ('email', models.CharField(max_length=100, verbose_name='Эл. почта')),
                ('password', models.CharField(max_length=30, verbose_name='Пароль')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.TextField(verbose_name='Задание')),
                ('correct_answer', models.TextField(verbose_name='Правильный ответ')),
                ('difficulty_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.difficulty_level', verbose_name='Уровень сложности')),
            ],
            options={
                'verbose_name': 'Задание',
                'verbose_name_plural': 'Задания',
            },
        ),
        migrations.AddField(
            model_name='difficulty_level',
            name='training_mode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.training_mode', verbose_name='Режим обучения'),
        ),
        migrations.AddField(
            model_name='training_mode',
            name='training_session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.training_session', verbose_name='Обучающая сессия'),
        ),
        migrations.AddField(
            model_name='training_session',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.user', verbose_name='Пользователь'),
        ),
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sound_grades', models.ManyToManyField(related_name='sound_translation', to='training.grades', verbose_name='Оценки по звучанию')),
                ('translation_grades', models.ManyToManyField(related_name='translation_grades', to='training.grades', verbose_name='Оценки по переводу')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Статистика',
                'verbose_name_plural': 'Статистики',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('settings', models.TextField(verbose_name='Настройки')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Настройки',
                'verbose_name_plural': 'Настройки',
            },
        ),
    ]
