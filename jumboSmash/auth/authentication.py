from rest_framework.authentication import TokenAuthentication as drf_TokenAuthentication


class TokenAuthentication(drf_TokenAuthentication):
    keyword = "Bearer"
