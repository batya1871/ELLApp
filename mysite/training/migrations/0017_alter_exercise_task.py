# Generated by Django 5.0.5 on 2024-05-10 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0016_alter_exercise_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='task',
            field=models.TextField(blank=True, default='Task in audio file', verbose_name='Задание'),
        ),
    ]
