from fastapi import APIRouter # type: ignore

from app.routes import well_routes
from app.routes import channel_data_routes
from app.routes import bucket_routes
from app.routes import bucket_generator_routes

api_router = APIRouter()

# Update the routing structure to follow a more RESTful hierarchy
api_router.include_router(
    well_routes.router, 
    prefix="/wells", 
    tags=["wells"]
)

api_router.include_router(
    channel_data_routes.router, 
    prefix="/wells/{well_id}/channels", 
    tags=["channels"]
)

api_router.include_router(
    bucket_routes.router, 
    prefix="/wells/{well_id}/channels/{channel_id}/data", 
    tags=["data"]
)

api_router.include_router(
    bucket_generator_routes.router, 
    prefix="/wells/{well_id}/channels/{channel_id}/generator", 
    tags=["data generation"]
)