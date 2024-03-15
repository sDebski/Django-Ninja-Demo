from ninja import Router
from http import HTTPStatus
from django.shortcuts import get_object_or_404

from company.schemas import LabelReadSchema, LabelWriteSchema
from company import models

router = Router(tags=["Labels"])


@router.get("", response={HTTPStatus.OK: list[LabelReadSchema]})
def get_labels(request):
    return HTTPStatus.OK, models.Label.objects.all()


@router.get("{id}/", response={HTTPStatus.OK: LabelReadSchema})
def get_label(request, id: int):
    label = get_object_or_404(models.Label, id=id)
    return HTTPStatus.OK, label


@router.post("", response={HTTPStatus.CREATED: LabelReadSchema})
def create_label(request, label_data: LabelWriteSchema):
    label_data = label_data.model_dump()
    return HTTPStatus.CREATED, models.Label.objects.create(**label_data)


@router.api_operation(
    ["PUT", "PATCH"], "{id}/", response={HTTPStatus.OK: LabelReadSchema}
)
def update_label(request, id: int, label_data: LabelWriteSchema):
    label = get_object_or_404(models.Label, id=id)
    label.name = label_data.name
    label.save()

    return HTTPStatus.OK, label


@router.delete("{id}/", response={HTTPStatus.NO_CONTENT: None})
def delete_label(request, id: int):
    label = get_object_or_404(models.Label, id=id)
    label.delete()

    return HTTPStatus.NO_CONTENT, None
