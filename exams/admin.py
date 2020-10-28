from django.contrib import admin

# Register your models here.
from exams import models

admin.site.register(models.ExamSeries)
# admin.site.register(models.Question)
# admin.site.register(models.Answer)

class AnswerInline(admin.TabularInline):
    model = models.Answer
    extra = 1
    max_num = 4
    # readonly_fields = ("toolcredential",)

    # def has_add_permission(self, request, obj=None):
    #     return False

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline, ]

admin.site.register(models.Question, QuestionAdmin)