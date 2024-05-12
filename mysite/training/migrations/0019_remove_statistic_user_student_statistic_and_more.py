# Generated by Django 5.0.5 on 2024-05-11 10:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0018_rename_translation_grades_statistic_translate_grades_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statistic',
            name='user',
        ),
        migrations.AddField(
            model_name='student',
            name='statistic',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to='training.statistic'),
        ),
        migrations.AlterField(
            model_name='difficulty_level',
            name='name',
            field=models.CharField(max_length=20, unique=True, verbose_name='Сложность'),
        ),
        migrations.AlterField(
            model_name='exercise_block',
            name='name',
            field=models.TextField(unique=True, verbose_name='Название теста'),
        ),
        migrations.AlterField(
            model_name='training_mode',
            name='name',
            field=models.CharField(max_length=10, unique=True, verbose_name='Название'),
        ),
    ]