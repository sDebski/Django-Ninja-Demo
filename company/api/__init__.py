from ninja import Router

from .label import router as label_router
from .worker import router as worker_router
from .projectcategory import router as projectcategory_router
from .task import router as task_router
from .project import router as project_router
from .comment import router as comment_router


router = Router()

router.add_router("labels/", label_router)
router.add_router("workers/", worker_router)
router.add_router("projectcategories/", projectcategory_router)
router.add_router("tasks/", task_router)
router.add_router("projects/", project_router)
router.add_router("comments/", comment_router)
