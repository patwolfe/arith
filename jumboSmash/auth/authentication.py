from rest_framework.authentication import TokenAuthentication as drf_TokenAuthentication
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from users.models import User


class TokenAuthentication(drf_TokenAuthentication):
    keyword = "Bearer"

    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)

        if user.status == User.REPORTED or user.status == User.BANNED:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        return user, token
