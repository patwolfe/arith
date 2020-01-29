from django.urls import include, path
from .views import Unmatch, SendMessage, GetConversation

urlpatterns = [
    path("unmatch", Unmatch.as_view()),
    path("send", SendMessage.as_view()),
    path("convo", GetConversation.as_view()),
]