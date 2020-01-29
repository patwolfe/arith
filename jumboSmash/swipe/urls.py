from django.urls import include, path
from swipe.views import GetNext, Smash, Skip, Refresh, BlockView

urlpatterns = [
    path("get_next/", GetNext.as_view()),
    path("smash/", Smash.as_view()),
    path("skip/", Skip.as_view()),
    path("refresh/", Refresh.as_view()),
    path("block/", BlockView.as_view()),
]
