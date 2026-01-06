from fastapi import APIRouter

from mealworm.api.routes.agents import agents_router
from mealworm.api.routes.health import health_router
from mealworm.api.routes.auth import auth_router
from mealworm.api.routes.preferences import preferences_router
# from mealworm.api.routes.playground import playground_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(health_router)
v1_router.include_router(auth_router)
v1_router.include_router(preferences_router)
v1_router.include_router(agents_router)
# v1_router.include_router(playground_router)
