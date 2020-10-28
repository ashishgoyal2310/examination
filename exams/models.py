from django.db import models
from django.utils.translation import gettext as _

# Create your models here.

class ExamSeries(models.Model):
    """
    """
    name = models.CharField(_("name"), max_length=64)
    code = models.CharField(_("code"), max_length=32, unique=True)
    valid_from = models.DateTimeField(_("valid from"), auto_now=False, auto_now_add=False)
    valid_to = models.DateTimeField(_("valid to"), auto_now=False, auto_now_add=False)
    correct_point = models.FloatField(_("correct answer point"), default=1)
    negative_point = models.FloatField(_("incorrect answer point"), default=0)
    enable_negative_marking = models.BooleanField(_("enable negative marking"), default=False)
    passing_percent = models.FloatField(_("passing percent"))


class Question(models.Model):
    """
    """
    uuid = models.CharField(_("uuid"), max_length=64, unique=True)
    desc = models.TextField(_("description"))
    desc_pre = models.TextField(_("description preformatted"), blank=True, default='')

    exam_series = models.ManyToManyField(
        'ExamSeries', 
        related_name='questions'
    )


class Answer(models.Model):
    """
    """
    desc = models.TextField(_("description"))
    is_correct = models.BooleanField(_('is correct'), default=False)

    exam_question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
        related_name="answers",
    )
