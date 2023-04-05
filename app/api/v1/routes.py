from fastapi import APIRouter
from .items import views as items_view
from .users import views as user_views

api_routers = APIRouter()

api_routers.include_router(items_view.router, tags=["items"], prefix="/items")
api_routers.include_router(user_views.router, tags=["users"], prefix="/users")
