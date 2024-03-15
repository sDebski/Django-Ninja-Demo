from ninja import ModelSchema, Schema
from devices import models


class LocationSchema(ModelSchema):
    class Meta:
        model = models.Location
        fields = "id", "name"


class DeviceSchema(ModelSchema):
    location: LocationSchema | None = None

    class Meta:
        model = models.Device
        fields = "id", "name", "slug", "location"


class DeviceCreateSchema(Schema):
    name: str
    location_id: int | None = None


class Error(Schema):
    message: str


class DeviceLocationPatch(Schema):
    location_id: int | None = None
