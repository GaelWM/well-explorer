from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query # type: ignore
from sqlalchemy.orm import Session # type: ignore

from app.core.database import get_db
from app.controllers.bucket_controller import BucketController
from app.schemas.bucket_schema import BucketDataOut, BucketDataCreate, BucketDataBatch, BucketStatistics

router = APIRouter()

@router.get("/wells/{well_name}/channel/{channel_name}", response_model=List[BucketDataOut])
def get_data_points(
    well_name: str,
    channel_name: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=10000),
    db: Session = Depends(get_db)
):
    """
    Retrieve time series data points from a bucket for a specific well and channel.
    """
    return BucketController.get_data_points(
        db, well_name, channel_name, start_date, end_date, skip, limit
    )

@router.post("/wells/{well_name}/channel/{channel_name}", response_model=BucketDataOut)
def create_data_point(
    well_name: str,
    channel_name: str,
    data_point: BucketDataCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new time series data point in a bucket.
    """
    return BucketController.create_data_point(db, well_name, channel_name, data_point)

@router.post("/wells/{well_name}/channel/{channel_name}/batch", response_model=List[BucketDataOut])
def create_data_points_batch(
    well_name: str,
    channel_name: str,
    data_points: BucketDataBatch,
    db: Session = Depends(get_db)
):
    """
    Create multiple time series data points in a bucket in a batch operation.
    """
    return BucketController.create_data_points_batch(db, well_name, channel_name, data_points)

@router.delete("/wells/{well_name}/channel/{channel_name}/point/{data_point_id}")
def delete_data_point(
    well_name: str,
    channel_name: str,
    data_point_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a specific time series data point from a bucket.
    """
    return BucketController.delete_data_point(db, well_name, channel_name, data_point_id)

@router.delete("/wells/{well_name}/channel/{channel_name}")
def delete_all_bucket_data(
    well_name: str,
    channel_name: str,
    db: Session = Depends(get_db)
):
    """
    Delete all time series data from a bucket.
    """
    return BucketController.delete_all_bucket_data(db, well_name, channel_name)

@router.get("/wells/{well_name}/channel/{channel_name}/statistics", response_model=BucketStatistics)
def get_statistics(
    well_name: str,
    channel_name: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """
    Get statistical information about time series data in a bucket.
    """
    return BucketController.get_statistics(db, well_name, channel_name, start_date, end_date)