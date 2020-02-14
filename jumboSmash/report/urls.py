from django.urls import path
from report.views import ReportView

urlpatterns = [
    path("", ReportView.as_view()),
]
