# Generated by Django 2.0 on 2020-10-28 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examseries',
            name='code',
            field=models.CharField(max_length=32, unique=True, verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='question',
            name='uuid',
            field=models.CharField(max_length=64, unique=True, verbose_name='uuid'),
        ),
    ]
