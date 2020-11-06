from django.shortcuts import render
from django.utils import timezone
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

from exams.models import ExamSeries, UserExam

# Create your views here.
class ExamSeriesView(TemplateView):
    template_name = "exam-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["exam_series"] = ExamSeries.objects.all().order_by('valid_from', 'valid_to', 'id')
        return context


class ExamSeriesDetailView(DetailView):
    slug_field = 'code'
    context_object_name = 'exam_series_obj'
    slug_url_kwarg = 'slug'

    model = ExamSeries
    template_name = 'exam-detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        exam_pin = request.POST.get('exam_pin')

        context = self.get_context_data(object=self.object)
        error_message = ""
        if timezone.now().date() < self.object.valid_from.date():
            error_message = 'Exam is not started yet.'
        elif timezone.now().date() > self.object.valid_to.date():
            error_message = 'Exam is already over.'

        user_exam = UserExam.objects.filter(exam_series=self.object, exam_pin=exam_pin).first()
        if not user_exam:
            error_message = 'Invalid exam pin.'

        if error_message:
            context['error_message'] = error_message
            return self.render_to_response(context)

        return self.render_to_response(context)