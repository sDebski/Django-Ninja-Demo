from ninja import Router

from .label import router as label_router
from .worker import router as worker_router
from .projectcategory import router as projectcategory_router


router = Router()

router.add_router("labels/", label_router)
router.add_router("workers/", worker_router)
router.add_router("projectcategories/", projectcategory_router)
