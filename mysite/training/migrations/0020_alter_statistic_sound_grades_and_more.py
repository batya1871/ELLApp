# Generated by Django 5.0.5 on 2024-05-11 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0019_remove_statistic_user_student_statistic_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistic',
            name='sound_grades',
            field=models.ManyToManyField(default=[], related_name='sound_grades', to='training.grades', verbose_name='Оценки по звучанию'),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='translate_grades',
            field=models.ManyToManyField(default=[], related_name='translation_grades', to='training.grades', verbose_name='Оценки по переводу'),
        ),
    ]
