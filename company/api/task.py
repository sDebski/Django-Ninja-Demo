from ninja import Router
from http import HTTPStatus
from django.shortcuts import get_object_or_404

from company.schemas import TaskWriteSchema, TaskReadSchema
from company import models

router = Router(tags=["Tasks"])


@router.get("", response={HTTPStatus.OK: list[TaskReadSchema]})
def get_tasks(request):
    return HTTPStatus.OK, models.Task.objects.all()


@router.get("{id}/", response={HTTPStatus.OK: TaskReadSchema})
def get_task(request, id: int):
    task = get_object_or_404(models.Task, id=id)
    return HTTPStatus.OK, task


@router.post(
    "",
    response={
        HTTPStatus.CREATED: TaskReadSchema,
        HTTPStatus.BAD_REQUEST: None,
    },
)
def create_task(request, task_data: TaskWriteSchema):
    worker = models.Worker.objects.filter(id=task_data.assigned_to)
    if not worker.exists():
        return HTTPStatus.BAD_REQUEST, None

    project = models.Project.objects.filter(id=task_data.project)
    if not project.exists():
        return HTTPStatus.BAD_REQUEST, None

    task_data = task_data.model_dump()
    return HTTPStatus.CREATED, models.Task.objects.create(**task_data)


@router.api_operation(
    ["PUT", "PATCH"],
    "{id}/",
    response={
        HTTPStatus.OK: TaskReadSchema,
        HTTPStatus.BAD_REQUEST: None,
    },
)
def update_task(request, id: int, task_data: TaskWriteSchema):
    task = get_object_or_404(models.Task, id=id)

    if task_data.assigned_to:
        worker = models.Worker.objects.filter(id=task_data.assigned_to)
        if not worker.exists():
            return HTTPStatus.BAD_REQUEST, None

    if task_data.project:
        project = models.Project.objects.filter(id=task_data.project)
        if not project.exists():
            return HTTPStatus.BAD_REQUEST, None

    for attr, value in task_data.dict().values():
        if value:
            setattr(task, attr, value)
    task.save()

    return HTTPStatus.OK, task


@router.delete("{id}/", response={HTTPStatus.NO_CONTENT: None})
def delete_task(request, id: int):
    task = get_object_or_404(models.Task, id=id)
    task.delete()

    return HTTPStatus.NO_CONTENT, None
