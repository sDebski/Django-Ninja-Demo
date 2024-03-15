from ninja import ModelSchema, Field
from company import models
from pydantic import validator


class LabelReadSchema(ModelSchema):
    class Meta:
        model = models.Label
        fields = "__all__"


class LabelWriteSchema(ModelSchema):
    name: str = Field("Default label name")

    class Meta:
        model = models.Label
        fields = ("name",)

    @validator("name")
    def name_must_contain_only_letters(cls, name):
        if not name.replace(" ", "").isalpha():
            raise ValueError("Name must contain only letters")
        return name
