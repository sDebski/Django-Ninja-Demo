from ninja import Router
from http import HTTPStatus
from django.shortcuts import get_object_or_404

from company.schemas import ProjectReadSchema, ProjectWriteSchema
from company import models

router = Router(tags=["Projects"])


@router.get("", response={HTTPStatus.OK: list[ProjectReadSchema]})
def get_projcts(request):
    return HTTPStatus.OK, models.Project.objects.all()


@router.get("{id}/", response={HTTPStatus.OK: ProjectReadSchema})
def get_project(request, id: int):
    project = get_object_or_404(models.Project, id=id)
    return HTTPStatus.OK, project


@router.post(
    "",
    response={
        HTTPStatus.CREATED: ProjectReadSchema,
        HTTPStatus.BAD_REQUEST: None,
    },
)
def create_project(request, project_data: ProjectWriteSchema):
    category = get_object_or_404(models.ProjectCategory, name=project_data.category)
    project_data = project_data.model_dump()
    project_data["category"] = category

    return HTTPStatus.CREATED, models.Project.objects.create(**project_data)


@router.api_operation(
    ["PUT", "PATCH"],
    "{id}/",
    response={
        HTTPStatus.OK: ProjectReadSchema,
        HTTPStatus.BAD_REQUEST: None,
    },
)
def update_project(request, id: int, project_data: ProjectWriteSchema):
    project = get_object_or_404(models.Project, id=id)

    project_data = project_data.dict()
    for attr, value in project_data.items():
        if value:
            setattr(project, attr, value)
    project.save()

    return HTTPStatus.OK, project


@router.delete("{id}/", response={HTTPStatus.NO_CONTENT: None})
def delete_project(request, id: int):
    project = get_object_or_404(models.Project, id=id)
    project.delete()

    return HTTPStatus.NO_CONTENT, None
