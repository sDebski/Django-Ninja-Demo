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
        category_names = [category["name"] for category in categories]
        if category not in category_names:
            raise TypeError(
                f'Project Category not valid. Available names: {", ".join(category_names)}.'
            )
        return category
