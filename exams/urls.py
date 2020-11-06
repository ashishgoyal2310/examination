from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from exams import views


urlpatterns = [
    url(r"^$", views.ExamSeriesView.as_view(), name="exam-series"),
    url(r"^(?P<slug>[\w-]+)/$", views.ExamSeriesDetailView.as_view(), name="exam-series-detail"),
]
