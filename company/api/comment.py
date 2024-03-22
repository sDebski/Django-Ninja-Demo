from ninja import Router
from http import HTTPStatus
from django.shortcuts import get_object_or_404

from company.schemas import CommentReadSchema, CommentWriteSchema
from company import models

router = Router(tags=["Comments"])


@router.get("", response={HTTPStatus.OK: list[CommentReadSchema]})
def get_comments(request):
    return HTTPStatus.OK, models.Comment.objects.all()


@router.get("{id}/", response={HTTPStatus.OK: CommentReadSchema})
def get_comment(request, id: int):
    comment = get_object_or_404(models.Comment, id=id)
    return HTTPStatus.OK, comment


@router.post(
    "",
    response={
        HTTPStatus.CREATED: CommentReadSchema,
        HTTPStatus.BAD_REQUEST: None,
    },
)
def create_comment(request, comment_data: CommentWriteSchema):
    comment_data = comment_data.model_dump()

    task = get_object_or_404(models.Task, id=comment_data["task"])
    comment_data["task"] = task

    return HTTPStatus.CREATED, models.Comment.objects.create(**comment_data)


@router.api_operation(
    ["PUT", "PATCH"],
    "{id}/",
    response={HTTPStatus.OK: CommentReadSchema},
)
def update_comment(request, id: int, comment_data: CommentWriteSchema):
    comment = get_object_or_404(models.Comment, id=id)

    task = get_object_or_404(models.Task, id=comment_data.task)
    comment.task = task

    comment.content = comment_data.content
    comment.save()

    return HTTPStatus.OK, comment


@router.delete("{id}/", response={HTTPStatus.NO_CONTENT: None})
def delete_comment(request, id: int):
    comment = get_object_or_404(models.Comment, id=id)
    comment.delete()

    return HTTPStatus.NO_CONTENT, None
