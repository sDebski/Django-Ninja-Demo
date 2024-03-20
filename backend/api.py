from ninja import NinjaAPI
from core.auth import ApiKeyAuth, KnoxAuth
from company.api import router as company_router
from devices.api import router as devices_router
from core.api import router as core_router


api = NinjaAPI(auth=[ApiKeyAuth(), KnoxAuth()])

api.add_router("auth/", core_router)
api.add_router("company/", company_router)
api.add_router("devices-api/", devices_router)
