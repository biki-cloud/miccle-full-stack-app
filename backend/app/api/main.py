from fastapi import APIRouter

from app.api.routes import (
    events,
    items,
    organizer_login,
    organizers,
    user_login,
    users,
    utils,
)

api_router = APIRouter()
api_router.include_router(user_login.router, tags=["user_login"])
api_router.include_router(organizer_login.router, tags=["organizer_login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(organizers.router, prefix="/organizers", tags=["organizers"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
