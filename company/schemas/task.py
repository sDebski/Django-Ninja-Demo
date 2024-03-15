from ninja import ModelSchema, Field, Schema
from company import models
from pydantic import validator


class TaskReadSchema(ModelSchema):
    class Meta:
        model = models.Task
        fields = "__all__"


class TaskWriteSchema(ModelSchema):
    title: str = None
    status: str = None
    description: str  = None
    project: int = None
    assigned_to: int = None
    labels: list[int] = None

    class Meta:
        model = models.Task
        fields = "title", "status", "description", "project", "assigned_to", "labels"

    @validator("status")
    def check_status(cls, status: str):
        statuses = ["Nowe", "W trakcie", "Zakończone"]
        if status not in statuses:
            raise TypeError(
                f'Status not valid. Available statuses: {", ".join(statuses)}.'
            )
        return status

    @validator("assigned_to")
    def check_worker_existance(cls, assigned_to: int):
        if not assigned_to:
            return assigned_to
        
        if not models.Worker.objects.filter(id=assigned_to).exists():
            return TypeError("Assigned_to id is not valid")
        return assigned_to

    @validator("project")
    def check_worker_existance(cls, project: int):
        if not project:
            return project
        
        if not models.Project.objects.filter(id=project).exists():
            return TypeError("Project id is not valid")
        return project

    @validator("title")
    def name_must_contain_only_letters(cls, title):
        if not title:
            return title
        if not title.replace(" ", "").isalpha():
            raise ValueError("Name must contain only letters")
        return title
