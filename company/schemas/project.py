from ninja import ModelSchema, Field, Schema
from company import models
from pydantic import validator


class ProjectReadSchema(ModelSchema):
    class Meta:
        model = models.Project
        fields = "__all__"


class ProjectWriteSchema(ModelSchema):
    name: str
    description: str
    category: str

    class Meta:
        model = models.Project
        fields = "name", "description", "category"

    @validator("category")
    def check_category(cls, category: str):
        categories = models.ProjectCategory.objects.all().values("name")
        print(categories)
        if category not in categories.values():
            raise TypeError(
                f'Project Category not valid. Available statuses: {", ".join(list(categories.values()))}.'
            )
        return category
