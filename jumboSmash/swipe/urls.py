from django.urls import include, path
from swipe.views import List, Smash, Skip, Refresh

urlpatterns = [
    path("list/", List.as_view()),
    path("smash/", Smash.as_view()),
    path("skip/", Skip.as_view()),
    path("refresh/", Refresh.as_view())
]