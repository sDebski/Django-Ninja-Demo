from http import HTTPStatus

from django.contrib.auth import authenticate
from knox.models import AuthToken
from ninja import Router
from core.schema import *

router = Router(tags=["Core"])


@router.post(
    "login/",
    response={
        HTTPStatus.OK: TokenResponseSchema,
        HTTPStatus.UNAUTHORIZED: UnauthorizedResponseSchema,
    },
    auth=None,
)
def login(request, credentials: LoginCredentialsSchema):
    user = authenticate(
        request,
        username=credentials.login,
        password=credentials.password,
    )

    if user:
        token_instance, token = AuthToken.objects.create(user)

        return HTTPStatus.OK, {
            "user": user,
            "token": token,
            "expiry": token_instance.expiry,
        }

    return HTTPStatus.UNAUTHORIZED, {"message": "Authentication failed"}
