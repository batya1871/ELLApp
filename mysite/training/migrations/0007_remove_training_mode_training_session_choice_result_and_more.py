# Generated by Django 5.0.5 on 2024-05-09 11:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0006_alter_training_mode_training_session'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='training_mode',
            name='training_session',
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_answer', models.TextField(verbose_name='Ответ пользователя')),
                ('Exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.exercise', verbose_name='Задание')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct', models.IntegerField(default=0, verbose_name='Кол-во правильных ответов')),
                ('wrong', models.IntegerField(default=0, verbose_name='Кол-во неправильных ответов')),
                ('training_mode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.training_mode', verbose_name='Режим обучения')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.DeleteModel(
            name='Training_session',
        ),
    ]
