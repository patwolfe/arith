from django.urls import include, path
from .views import Unmatch, SendMessage, GetConversation, GetAll, ViewConversation

urlpatterns = [
    path("unmatch/", Unmatch.as_view()),
    path("send/", SendMessage.as_view()),
    path("convo/", GetConversation.as_view()),
    path("all/", GetAll.as_view()),
    path("view/", ViewConversation.as_view()),
]
