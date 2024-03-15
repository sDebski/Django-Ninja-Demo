from ninja import ModelSchema, Field
from company import models
from pydantic import EmailStr


class WorkerReadSchema(ModelSchema):
    class Meta:
        model = models.Worker
        fields = "__all__"


class WorkerWriteSchema(ModelSchema):
    email: EmailStr
    username: str = Field("username")

    class Meta:
        model = models.Worker
        fields = (
            "email",
            "username",
        )
