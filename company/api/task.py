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
    worker = models.Worker.objects.filter(id=task_data.assigned_to).first()
    if not worker:
        return HTTPStatus.BAD_REQUEST, None

    project = models.Project.objects.filter(id=task_data.project).first()
    if not project:
        return HTTPStatus.BAD_REQUEST, None

    task_data = task_data.model_dump()

    task_data["assigned_to"] = worker
    task_data["project"] = project

    labels = task_data.pop("labels")
    task = models.Task.objects.create(**task_data)
    task.labels.set(labels)

    return HTTPStatus.CREATED, task


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
        worker = models.Worker.objects.filter(id=task_data.assigned_to).first()
        if not worker:
            return HTTPStatus.BAD_REQUEST, None
        task_data.assigned_to = worker

    if task_data.project:
        project = models.Project.objects.filter(id=task_data.project).first()
        if not project:
            return HTTPStatus.BAD_REQUEST, None
        task_data.project = project

    task_data = task_data.dict()
    labels = task_data.pop("labels")
    for attr, value in task_data.items():
        if value:
            setattr(task, attr, value)
    task.save()
    task.labels.set(labels)

    return HTTPStatus.OK, task


@router.delete("{id}/", response={HTTPStatus.NO_CONTENT: None})
def delete_task(request, id: int):
    task = get_object_or_404(models.Task, id=id)
    task.delete()

    return HTTPStatus.NO_CONTENT, None
