from django.contrib import admin

# Register your models here.
from exams import models

admin.site.register(models.ExamSeries)
admin.site.register(models.UserExam)
admin.site.register(models.UserQuestion)

class AnswerInline(admin.TabularInline):
    model = models.Answer
    extra = 1
    max_num = 4

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'rank',)
    list_filter = ('exam_series',)
    list_editable = ('rank',)
    inlines = [AnswerInline, ]

admin.site.register(models.Question, QuestionAdmin)