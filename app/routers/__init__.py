from fastapi import APIRouter

from app.routers.auth import router as auth_router
from app.routers.user import router as user_router
from app.routers.animals import router as animal_router
from app.routers.example_route import router as example_router


router = APIRouter(prefix='/v1')

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(animal_router)
router.include_router(example_router)
