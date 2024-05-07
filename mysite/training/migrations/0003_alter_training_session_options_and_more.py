# Generated by Django 5.0.5 on 2024-05-07 13:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0002_alter_statistic_sound_grades'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='training_session',
            options={'verbose_name': 'Обучающая сессия', 'verbose_name_plural': 'Обучающие сессии'},
        ),
        migrations.AlterField(
            model_name='difficulty_level',
            name='training_mode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.training_mode', verbose_name='Уровень сложности'),
        ),
    ]
