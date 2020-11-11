import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, login

from exams.models import ExamSeries, UserExam, UserQuestion, Question, Answer

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
        elif not Question.objects.filter(exam_series=user_exam.exam_series).exists():
            error_message = 'Questions are not ready for this exam.'

        if error_message:
            context['error_message'] = error_message
            return self.render_to_response(context)

        login(request, user_exam.user)
        self.template_name = "exam-question.html"
        context['user_exam'] = user_exam
        return self.render_to_response(context)


class UserExamQuestionApiView(View):

    def fetch_next_question_data(self, user_exam, question_id=None):
        questions = user_exam.exam_series.questions.all().order_by('rank')
        question = None if not question_id else questions.filter(id=question_id).first()

        if not question:
            user_question_last_attempted = user_exam.user_questions.order_by('updated_at').last()
            if user_question_last_attempted:
                filtered_questions = questions.filter(rank__gt=user_question_last_attempted.question.rank)
                question = filtered_questions.first() if filtered_questions else user_question_last_attempted.question
            else:
                question = questions.first()

        prev_question = questions.filter(rank__lt=question.rank).last()
        prev_question_id = prev_question.id if prev_question else ''
        is_last = question == questions.last()

        user_question = user_exam.user_questions.filter(question=question).first()
        user_question_answer = getattr(user_question, 'answer', None)
        answers = question.answers.all().order_by('?')
        answer_data = [{'id': _.id, 'desc': _.desc, 'is_selected': _ == user_question_answer} for _ in answers]

        return {
            'id': user_exam.id, 'code': user_exam.exam_series.code,
            'prev_question_id': prev_question_id, 'is_last': is_last,
            'question_id': question.id, 'question_desc': question.desc, 'answer_data': answer_data
        }

    def get(self, request, pk, *args, **kwargs):
        user_exam = UserExam.objects.filter(user=request.user, pk=pk).first()
        if not user_exam:
            return JsonResponse({'message': 'Bad Request from server (User Exam).'}, safe=False, status=400)

        try:
            question_id = int(request.GET.get('question_id', ''))
        except Exception as exc:
            question_id = ''

        _response_data = self.fetch_next_question_data(user_exam, question_id=question_id)

        return JsonResponse(_response_data, safe=False)

    def post(self, request, pk, *args, **kwargs):
        user_exam = UserExam.objects.filter(user=request.user, pk=pk).first()
        if not user_exam:
            return JsonResponse({'message': 'Bad Request from server (User Exam).'}, safe=False, status=400)

        try:
            post_data = json.loads(request.body)
        except Exception as exc:
            return JsonResponse({'message': 'Bad Request from server (Post data).'}, safe=False, status=400)

        try:
            UserQuestion.objects.update_or_create(
                user_exam=user_exam, question_id=post_data['question_id'],
                defaults={
                    'answer_id': post_data.get('answer_id', None),
                    'is_marked': True if post_data.get('is_marked', False) else False,
                    'is_answered': True if post_data.get('answer_id', False) else False,
                }
            )
        except Exception as exc:
            return JsonResponse({'message': 'Bad Request from server (Answer Submit).'}, safe=False, status=400)

        _response_data = self.fetch_next_question_data(user_exam)

        return JsonResponse(_response_data, safe=False)


class ScreenView(TemplateView):
    template_name = "exam-question.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_exam'] = UserExam.objects.filter().first()
        return context