# Generated by Django 5.0.5 on 2024-05-12 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0020_alter_statistic_sound_grades_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='processed',
            field=models.BooleanField(default=False, verbose_name='Это поле обработано'),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='sound_grades',
            field=models.ManyToManyField(related_name='sound_grades', to='training.grades', verbose_name='Оценки по звучанию'),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='translate_grades',
            field=models.ManyToManyField(related_name='translation_grades', to='training.grades', verbose_name='Оценки по переводу'),
        ),
    ]