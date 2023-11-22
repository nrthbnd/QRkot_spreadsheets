from fastapi import APIRouter

from constants import (
    CHARITY_PROJECT_ROUTER_PREFIX, CHARITY_PROJECT_ROUTER_TAG,
    DONATION_ROUTER_PREFIX, DONATION_ROUTER_TAG,
    GOOGLE_ROUTER_PREFIX, GOOGLE_ROUTER_TAG,
)
from app.api.endpoints import (
    google_api_router, charity_project_router, donation_router, user_router,
)


main_router = APIRouter()

main_router.include_router(
    charity_project_router,
    prefix=CHARITY_PROJECT_ROUTER_PREFIX,
    tags=[CHARITY_PROJECT_ROUTER_TAG],
)

main_router.include_router(
    donation_router,
    prefix=DONATION_ROUTER_PREFIX,
    tags=[DONATION_ROUTER_TAG],
)
main_router.include_router(
    google_api_router,
    prefix=GOOGLE_ROUTER_PREFIX,
    tags=[GOOGLE_ROUTER_TAG],
)
main_router.include_router(user_router)
