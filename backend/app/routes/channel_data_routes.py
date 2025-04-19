from typing import List
from fastapi import APIRouter, Depends, Query, Path # type: ignore
from sqlalchemy.orm import Session # type: ignore

from app.core.database import get_db
from app.controllers.channel_data_controller import ChannelDataController
from app.schemas.channel_data_schema import ChannelData, ChannelDataCreate, ChannelDataUpdate, ChannelDataExtended 

router = APIRouter()

@router.get("/", response_model=List[ChannelData])
def get_channels_by_well_id(
    well_id: int = Path(..., description="The ID of the well"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Retrieve all channels for a specific well.
    """
    return ChannelDataController.get_channels_by_well_id(db, well_id=well_id)

@router.get("/{channel_id}", response_model=ChannelDataExtended)
def get_channel(
    well_id: int = Path(..., description="The ID of the well"),
    channel_id: int = Path(..., description="The ID of the channel"),
    db: Session = Depends(get_db)
):
    """
    Get a specific channel by ID.
    """
    return ChannelDataController.get_channel_by_id(db, channel_id=channel_id)

@router.get("/name/{name}", response_model=ChannelDataExtended)
def get_channel_by_well_and_name(
    name: str,
    well_id: int = Path(..., description="The ID of the well"), 
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific channel by well ID and channel name.
    Returns extended info including bucket name.
    """
    return ChannelDataController.get_channel_by_well_and_name(db, well_id=well_id, name=name)

@router.post("/", response_model=ChannelDataExtended)
def create_channel(
    channel: ChannelDataCreate,
    well_id: int = Path(..., description="The ID of the well"),
    db: Session = Depends(get_db)
):
    """
    Create a new channel for the specified well.
    Returns extended info including bucket name.
    """
    # Ensure the well_id in the path matches the one in the request
    if channel.well_id != well_id:
        # Override the well_id in the request with the one from the path
        channel.well_id = well_id
        
    return ChannelDataController.create_channel(db, channel=channel)

@router.put("/{channel_id}", response_model=ChannelDataExtended)
def update_channel(
    channel_update: ChannelDataUpdate,
    well_id: int = Path(..., description="The ID of the well"),
    channel_id: int = Path(..., description="The ID of the channel"), 
    db: Session = Depends(get_db)
):
    """
    Update a channel.
    Returns extended info including bucket name.
    """
    return ChannelDataController.update_channel(db, channel_id=channel_id, channel_update=channel_update)

@router.delete("/{channel_id}")
def delete_channel(
    well_id: int = Path(..., description="The ID of the well"),
    channel_id: int = Path(..., description="The ID of the channel"),
    db: Session = Depends(get_db)
):
    """
    Delete a channel.
    """
    return ChannelDataController.delete_channel(db, channel_id=channel_id)