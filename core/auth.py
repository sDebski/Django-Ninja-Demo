from typing import Any
from django.http import HttpRequest
from knox.auth import TokenAuthentication as KnoxTokenAuthentication
from ninja.security import APIKeyHeader, HttpBearer


class ApiKeyAuth(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request: HttpRequest, key: str | None) -> Any | None:
        if key == "classified":
            return key


class KnoxAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> Any | None:
        knox_auth = KnoxTokenAuthentication()
        try:
            user_auth_tuple = knox_auth.authenticate_credentials(token.encode("utf-8"))
        except:
            return

        if user_auth_tuple is not None:
            return user_auth_tuple[0]
