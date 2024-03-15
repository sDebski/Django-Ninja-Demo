from ninja import Router
from http import HTTPStatus
from django.shortcuts import get_object_or_404

from company.schemas import WorkerReadSchema, WorkerWriteSchema
from company import models

router = Router(tags=["Workers"])


@router.get("", response={HTTPStatus.OK: list[WorkerReadSchema]})
def get_workers(request):
    return HTTPStatus.OK, models.Worker.objects.all()


@router.get("{id}/", response={HTTPStatus.OK: WorkerReadSchema})
def get_worker(request, id: int):
    worker = get_object_or_404(models.Worker, id=id)
    return HTTPStatus.OK, worker


@router.post(
    "",
    response={
        HTTPStatus.CREATED: WorkerReadSchema,
        HTTPStatus.BAD_REQUEST: None,
    },
)
def create_worker(request, worker_data: WorkerWriteSchema):
    user_with_email = models.Worker.objects.filter(email=worker_data.email)
    if user_with_email.exists():
        return HTTPStatus.BAD_REQUEST, None

    worker_data = worker_data.model_dump()
    return HTTPStatus.CREATED, models.Worker.objects.create(**worker_data)


@router.api_operation(
    ["PUT", "PATCH"],
    "{id}/",
    response={
        HTTPStatus.OK: WorkerReadSchema,
        HTTPStatus.BAD_REQUEST: None,
    },
)
def update_worker(request, id: int, worker_data: WorkerWriteSchema):
    worker = get_object_or_404(models.Worker, id=id)
    user_with_email = models.Worker.objects.filter(email=worker_data.email).exclude(
        id=id
    )
    if user_with_email.exists():
        return HTTPStatus.BAD_REQUEST, None

    worker.username = worker_data.username
    worker.email = worker_data.email
    worker.save()

    return HTTPStatus.OK, worker


@router.delete("{id}/", response={HTTPStatus.NO_CONTENT: None})
def delete_worker(request, id: int):
    worker = get_object_or_404(models.Worker, id=id)
    worker.delete()

    return HTTPStatus.NO_CONTENT, None
