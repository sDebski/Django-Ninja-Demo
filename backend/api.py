from ninja import NinjaAPI
from company.api import router as company_router
from devices.api import router as devices_router


api = NinjaAPI()

api.add_router("company/", company_router)
api.add_router("devices-api/", devices_router)
