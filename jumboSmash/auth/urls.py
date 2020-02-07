from django.urls import include, path
from .views import Logout

urlpatterns = [
    path("", include("drfpasswordless.urls")),
    path("logout/", Logout.as_view()),
]
