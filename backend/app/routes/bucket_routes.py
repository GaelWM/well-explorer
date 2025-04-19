from http.client import HTTPException
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query, Path # type: ignore
from sqlalchemy.orm import Session # type: ignore

from app.core.database import get_db
from app.controllers.bucket_controller import BucketController
from app.repositories.channel_data_repository import ChannelDataRepository
from app.schemas.bucket_schema import BucketDataOut, BucketDataCreate, BucketDataBatch, BucketStatistics

router = APIRouter()

# Helper function to get well_name and channel_name from IDs
async def get_names_from_ids(well_id: int, channel_id: int, db: Session):
    channel = ChannelDataRepository.get_channel_by_id(db, channel_id)
    if not channel or channel.well_id != well_id:
        return None, None
    return channel.well.name, channel.name

@router.get("/", response_model=List[BucketDataOut])
async def get_data_points(
    well_id: int = Path(..., description="The ID of the well"),
    channel_id: int = Path(..., description="The ID of the channel"),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=10000),
    db: Session = Depends(get_db)
):
    """
    Retrieve time series data points for a specific channel.
    """
    well_name, channel_name = await get_names_from_ids(well_id, channel_id, db)
    if not well_name or not channel_name:
        raise HTTPException(status_code=404, detail=f"Channel with id {channel_id} not found for well {well_id}")
    
    return BucketController.get_data_points(
        db, well_name, channel_name, start_date, end_date, skip, limit
    )

@router.post("/", response_model=BucketDataOut)
async def create_data_point(
    data_point: BucketDataCreate,
    well_id: int = Path(..., description="The ID of the well"),
    channel_id: int = Path(..., description="The ID of the channel"),
    db: Session = Depends(get_db)
):
    """
    Create a new time series data point.
    """
    well_name, channel_name = await get_names_from_ids(well_id, channel_id, db)
    if not well_name or not channel_name:
        raise HTTPException(status_code=404, detail=f"Channel with id {channel_id} not found for well {well_id}")
    
    return BucketController.create_data_point(db, well_name, channel_name, data_point)

@router.post("/batch", response_model=List[BucketDataOut])
async def create_data_points_batch(
    data_points: BucketDataBatch,
    well_id: int = Path(..., description="The ID of the well"),
    channel_id: int = Path(..., description="The ID of the channel"),
    db: Session = Depends(get_db)
):
    """
    Create multiple time series data points in a batch operation.
    """
    well_name, channel_name = await get_names_from_ids(well_id, channel_id, db)
    if not well_name or not channel_name:
        raise HTTPException(status_code=404, detail=f"Channel with id {channel_id} not found for well {well_id}")
    
    return BucketController.create_data_points_batch(db, well_name, channel_name, data_points)

@router.delete("/{data_point_id}")
async def delete_data_point(
    data_point_id: int,
    well_id: int = Path(..., description="The ID of the well"),
    channel_id: int = Path(..., description="The ID of the channel"),
    db: Session = Depends(get_db)
):
    """
    Delete a specific time series data point.
    """
    well_name, channel_name = await get_names_from_ids(well_id, channel_id, db)
    if not well_name or not channel_name:
        raise HTTPException(status_code=404, detail=f"Channel with id {channel_id} not found for well {well_id}")
    
    return BucketController.delete_data_point(db, well_name, channel_name, data_point_id)

@router.delete("/")
async def delete_all_bucket_data(
    well_id: int = Path(..., description="The ID of the well"),
    channel_id: int = Path(..., description="The ID of the channel"),
    db: Session = Depends(get_db)
):
    """
    Delete all time series data for a specific channel.
    """
    well_name, channel_name = await get_names_from_ids(well_id, channel_id, db)
    if not well_name or not channel_name:
        raise HTTPException(status_code=404, detail=f"Channel with id {channel_id} not found for well {well_id}")
    
    return BucketController.delete_all_bucket_data(db, well_name, channel_name)

@router.get("/statistics", response_model=BucketStatistics)
async def get_statistics(
    well_id: int = Path(..., description="The ID of the well"),
    channel_id: int = Path(..., description="The ID of the channel"),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """
    Get statistical information about time series data.
    """
    well_name, channel_name = await get_names_from_ids(well_id, channel_id, db)
    if not well_name or not channel_name:
        raise HTTPException(status_code=404, detail=f"Channel with id {channel_id} not found for well {well_id}")
    
    return BucketController.get_statistics(db, well_name, channel_name, start_date, end_date)