from django.urls import include, path
from .views import Unmatch

urlpatterns = [
    path("unmatch", Unmatch.as_view()),
]