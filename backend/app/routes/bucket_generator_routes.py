from typing import Optional, Dict, Any
from datetime import datetime
from fastapi import APIRouter, Depends, Query, Body, Path # type: ignore
from sqlalchemy.orm import Session # type: ignore
from pydantic import BaseModel, Field # type: ignore
from fastapi import HTTPException # type: ignore

from app.core.database import get_db
from app.repositories.bucket_generator_repository import BucketDataGenerator
from app.repositories.channel_data_repository import ChannelDataRepository

router = APIRouter()

class PatternDataRequest(BaseModel):
    pattern_type: str = Field(default="sine", description="Pattern type: sine, cosine, sawtooth, square, random, trend")
    start_date: Optional[datetime] = Field(default=None, description="Start date (defaults to 30 days ago)")
    end_date: Optional[datetime] = Field(default=None, description="End date (defaults to current date)")
    interval_seconds: int = Field(default=3600, description="Time interval between points in seconds")
    base_value: float = Field(default=50.0, description="Base value for the data")
    amplitude: float = Field(default=25.0, description="Amplitude of the pattern")
    period_days: float = Field(default=7.0, description="Period of the pattern in days")
    trend_slope: float = Field(default=0.0, description="Slope of the trend (units per day)")
    noise_level: float = Field(default=2.0, description="Magnitude of random noise")

# Helper function to get well_name and channel_name from IDs
async def get_names_from_ids(well_id: int, channel_id: int, db: Session):
    channel = ChannelDataRepository.get_channel_by_id(db, channel_id)
    if not channel or channel.well_id != well_id:
        return None, None
    return channel.well.name, channel.name

@router.post("/pattern", response_model=Dict[str, Any])
async def generate_bucket_data(
    request: PatternDataRequest,
    well_id: int = Path(..., description="The ID of the well"),
    channel_id: int = Path(..., description="The ID of the channel"),
    db: Session = Depends(get_db)
):
    """
    Generate time series data with specific patterns.
    """
    well_name, channel_name = await get_names_from_ids(well_id, channel_id, db)
    if not well_name or not channel_name:
        raise HTTPException(status_code=404, detail=f"Channel with id {channel_id} not found for well {well_id}")
    
    return BucketDataGenerator.generate_pattern_data(
        db=db,
        well_name=well_name,
        channel_name=channel_name,
        pattern_type=request.pattern_type,
        start_date=request.start_date,
        end_date=request.end_date,
        interval_seconds=request.interval_seconds,
        base_value=request.base_value,
        amplitude=request.amplitude,
        period_days=request.period_days,
        trend_slope=request.trend_slope,
        noise_level=request.noise_level
    )

@router.post("/populate", response_model=Dict[str, Any])
async def populate_bucket(
    well_id: int = Path(..., description="The ID of the well"),
    channel_id: int = Path(..., description="The ID of the channel"),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    interval_seconds: int = Query(3600, description="Time interval between points in seconds"),
    db: Session = Depends(get_db)
):
    """
    Populate a bucket with time series data at regular intervals using default sine wave pattern.
    """
    well_name, channel_name = await get_names_from_ids(well_id, channel_id, db)
    if not well_name or not channel_name:
        raise HTTPException(status_code=404, detail=f"Channel with id {channel_id} not found for well {well_id}")
    
    return BucketDataGenerator.populate_bucket(
        db=db,
        well_name=well_name,
        channel_name=channel_name,
        start_date=start_date,
        end_date=end_date,
        interval_seconds=interval_seconds
    )