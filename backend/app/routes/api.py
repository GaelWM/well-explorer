from fastapi import APIRouter # type: ignore

from app.routes import well_routes
from app.routes import channel_data_routes
from app.routes import bucket_routes

api_router = APIRouter()

api_router.include_router(well_routes.router, prefix="/wells", tags=["wells"])
api_router.include_router(channel_data_routes.router, prefix="/channels", tags=["channels"])
api_router.include_router(bucket_routes.router, prefix="/buckets", tags=["buckets"])