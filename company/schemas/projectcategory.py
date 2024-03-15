from ninja import ModelSchema, Field
from company import models
from pydantic import validator


class ProjectCategoryReadSchema(ModelSchema):
    class Meta:
        model = models.ProjectCategory
        fields = "__all__"


class ProjectCategoryWriteSchema(ModelSchema):
    name: str = Field("Default ProjectCategory name")

    class Meta:
        model = models.ProjectCategory
        fields = ("name",)

    @validator("name")
    def name_must_contain_only_letters(cls, name):
        if not name.replace(" ", "").isalpha():
            raise ValueError("Name must contain only letters")
        return name
