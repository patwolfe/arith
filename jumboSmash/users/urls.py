from django.urls import include, path
from users.views import ListUsers, GetProfile, EditProfile, CheckUserExists, UpdateToken, SetupUser

urlpatterns = [
    path("list/", ListUsers.as_view()),
    path("profile/", GetProfile.as_view()),
    path("profile/edit/", EditProfile.as_view()),
    path("check/", CheckUserExists.as_view()),
    path("push_token/", UpdateToken.as_view()),
    path("setup/", SetupUser.as_view()),
]
