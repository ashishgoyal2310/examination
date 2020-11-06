from django.db import models
from django.utils.translation import gettext as _

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class ExamSeries(models.Model):
    """
    """
    name = models.CharField(_("name"), max_length=64)
    code = models.CharField(_("code"), max_length=32, unique=True)
    valid_from = models.DateTimeField(_("valid from"), auto_now=False, auto_now_add=False)
    valid_to = models.DateTimeField(_("valid to"), auto_now=False, auto_now_add=False)
    duration = models.IntegerField(_("duration (minutes)"), default=0)
    correct_point = models.FloatField(_("correct answer point"), default=1)
    negative_point = models.FloatField(_("incorrect answer point"), default=0)
    enable_negative_marking = models.BooleanField(_("enable negative marking"), default=False)
    passing_percent = models.FloatField(_("passing percent"))

    def __str__(self):
        return '%s - %s' %(self.name,self.code)


class Question(models.Model):
    """
    """
    rank = models.IntegerField(_("rank"), unique=True)
    desc = models.TextField(_("description"))

    exam_series = models.ManyToManyField(
        'ExamSeries',
        related_name='questions'
    )

    def __str__(self):
        return '%s - %s' %('Question', self.rank)


class Answer(models.Model):
    """
    """
    desc = models.TextField(_("description"))
    is_correct = models.BooleanField(_('is correct'), default=False)

    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
        related_name="answers",
    )


class UserExam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_exams')
    exam_series = models.ForeignKey('ExamSeries', on_delete=models.CASCADE, related_name='user_exams')

    exam_pin = models.CharField(_('exam pin'), max_length=8, unique=True)

    started_at = models.DateTimeField(_("valid from"), auto_now=False, auto_now_add=False)
    ended_at = models.DateTimeField(_("valid from"), auto_now=False, auto_now_add=False)


class UserQuestion(models.Model):
    user_exam = models.ForeignKey('UserExam', on_delete=models.CASCADE, related_name='user_questions')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='user_questions')
    answer = models.ForeignKey('Answer', on_delete=models.SET_NULL, related_name='user_questions', null=True)

    is_marked = models.BooleanField(_('marked for review'), default=False)
    is_answered = models.BooleanField(_('answer marked'), default=False)
