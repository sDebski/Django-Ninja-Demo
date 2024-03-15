from ninja import Router
from http import HTTPStatus
from django.shortcuts import get_object_or_404

from company.schemas import ProjectCategoryReadSchema, ProjectCategoryWriteSchema
from company import models

router = Router(tags=["ProjectCategories"])


@router.get("", response={HTTPStatus.OK: list[ProjectCategoryReadSchema]})
def get_projectcategories(request):
    return HTTPStatus.OK, models.ProjectCategory.objects.all()


@router.get("{id}/", response={HTTPStatus.OK: ProjectCategoryReadSchema})
def get_projectcategory(request, id: int):
    projectcategory = get_object_or_404(models.ProjectCategory, id=id)
    return HTTPStatus.OK, projectcategory


@router.post(
    "",
    response={
        HTTPStatus.CREATED: ProjectCategoryReadSchema,
        HTTPStatus.BAD_REQUEST: None,
    },
)
def create_projectcategory(request, projectcategory_data: ProjectCategoryWriteSchema):
    projectcategory_data = projectcategory_data.model_dump()
    return HTTPStatus.CREATED, models.ProjectCategory.objects.create(
        **projectcategory_data
    )


@router.api_operation(
    ["PUT", "PATCH"],
    "{id}/",
    response={HTTPStatus.OK: ProjectCategoryReadSchema},
)
def update_projectcategory(
    request, id: int, projectcategory_data: ProjectCategoryWriteSchema
):
    projectcategory = get_object_or_404(models.ProjectCategory, id=id)
    projectcategory.name = projectcategory_data.name
    projectcategory.save()

    return HTTPStatus.OK, projectcategory


@router.delete("{id}/", response={HTTPStatus.NO_CONTENT: None})
def delete_projectcategory(request, id: int):
    projectcategory = get_object_or_404(models.ProjectCategory, id=id)
    projectcategory.delete()

    return HTTPStatus.NO_CONTENT, None
