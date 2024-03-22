from ninja import ModelSchema, Field
from company import models
from pydantic import validator


class CommentReadSchema(ModelSchema):
    class Meta:
        model = models.Comment
        fields = "__all__"


class CommentWriteSchema(ModelSchema):
    content: str = Field("Default content")
    task: int

    class Meta:
        model = models.Comment
        fields = ("content",)

    @validator("task")
    def check_task(cls, task_id):
        task = models.Task.objects.filter(id=task_id).first()
        if not task:
            raise TypeError("Task ID not valid.")
        return task_id