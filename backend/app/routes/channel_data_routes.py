from typing import List
from fastapi import APIRouter, Depends, Query # type: ignore
from sqlalchemy.orm import Session # type: ignore

from app.core.database import get_db
from app.controllers.channel_data_controller import ChannelDataController
from app.schemas.channel_data_schema import ChannelData, ChannelDataCreate, ChannelDataUpdate

router = APIRouter()

@router.get("/", response_model=List[ChannelData])
def get_channels(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """
    Retrieve all channels with pagination.
    """
    return ChannelDataController.get_channels(db, skip=skip, limit=limit)

@router.get("/wells/{well_id}/channels", response_model=List[ChannelData])
def get_channels_by_well_id(
    well_id: int, 
    db: Session = Depends(get_db)
):
    """
    Retrieve all channels for a specific well.
    """
    return ChannelDataController.get_channels_by_well_id(db, well_id=well_id)

@router.get("/wells/{well_id}/channels/{channel_id}", response_model=ChannelData)
def get_channel(
    channel_id: int, 
    db: Session = Depends(get_db)
):
    """
    Get a specific channel by ID.
    """
    return ChannelDataController.get_channel_by_id(db, channel_id=channel_id)


@router.post("/wells/{well_id}/channels", response_model=ChannelData)
def create_channel(
    channel: ChannelDataCreate, 
    db: Session = Depends(get_db)
):
    """
    Create a new channel.
    """
    return ChannelDataController.create_channel(db, channel=channel)

@router.put("/wells/{well_id}/channels/{channel_id}", response_model=ChannelData)
def update_channel(
    channel_id: int, 
    channel_update: ChannelDataUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update a channel.
    """
    return ChannelDataController.update_channel(db, channel_id=channel_id, channel_update=channel_update)

@router.delete("/wells/{well_id}/channels/{channel_id}")
def delete_channel(
    channel_id: int, 
    db: Session = Depends(get_db)
):
    """
    Delete a channel.
    """
    return ChannelDataController.delete_channel(db, channel_id=channel_id)