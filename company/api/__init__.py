from ninja import Router

from .label import router as label_router

router = Router()

router.add_router("labels/", label_router)
