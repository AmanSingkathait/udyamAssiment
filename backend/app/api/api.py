from fastapi import APIRouter
from app.api.endpoints import registration

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(registration.router, prefix="/registration", tags=["registration"]) 