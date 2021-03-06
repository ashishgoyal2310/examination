# Generated by Django 2.0 on 2020-10-28 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField(verbose_name='description')),
                ('is_correct', models.BooleanField(default=False, verbose_name='is correct')),
            ],
        ),
        migrations.CreateModel(
            name='ExamSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='name')),
                ('code', models.CharField(max_length=32, verbose_name='code')),
                ('valid_from', models.DateTimeField(verbose_name='valid from')),
                ('valid_to', models.DateTimeField(verbose_name='valid to')),
                ('correct_point', models.FloatField(default=1, verbose_name='correct answer point')),
                ('negative_point', models.FloatField(default=0, verbose_name='incorrect answer point')),
                ('enable_negative_marking', models.BooleanField(default=False, verbose_name='enable negative marking')),
                ('passing_percent', models.FloatField(verbose_name='passing percent')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=64, verbose_name='uuid')),
                ('desc', models.TextField(verbose_name='description')),
                ('desc_pre', models.TextField(verbose_name='description preformatted')),
                ('exam_series', models.ManyToManyField(related_name='questions', to='exams.ExamSeries')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='exam_question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='exams.Question'),
        ),
    ]
