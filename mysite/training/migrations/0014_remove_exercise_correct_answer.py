# Generated by Django 5.0.5 on 2024-05-10 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0013_correct_answers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise',
            name='correct_answer',
        ),
    ]