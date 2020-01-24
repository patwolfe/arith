from django.urls import include, path
from matches.views import Unmatch

urlpatterns = [
    path("unmatch", Unmatch.as_view()),
]