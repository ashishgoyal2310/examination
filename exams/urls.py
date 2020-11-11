from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from exams import views


urlpatterns = [
    url(r"^$", views.ExamSeriesView.as_view(), name="exam-series"),
    # url(r"^screen/$", views.ScreenView.as_view(), name="screen-view"),
    url(r"^(?P<slug>[\w-]+)/$", views.ExamSeriesDetailView.as_view(), name="exam-series-detail"),

    url(r"^user-exam/(?P<pk>\d+)/question/$", views.UserExamQuestionApiView.as_view(), name="user-exam-question"),
    url(r"^user-exam/(?P<pk>\d+)/question-palette/$", views.UserExamQuestionPaletteApiView.as_view(), name="user-exam-question-palette"),
]
