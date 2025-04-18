from typing import List, Optional
from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import func # type: ignore

from app.models.channel_data import ChannelData
from app.models.well import Well
from app.schemas.channel_data_schema import ChannelDataCreate, ChannelDataUpdate

class ChannelDataRepository:
    @staticmethod
    def get_channels(db: Session, skip: int = 0, limit: int = 100) -> List[ChannelData]:
        return db.query(ChannelData).offset(skip).limit(limit).all()

    @staticmethod
    def get_channel_by_id(db: Session, channel_id: int) -> Optional[ChannelData]:
        return db.query(ChannelData).filter(ChannelData.id == channel_id).first()

    @staticmethod
    def get_channels_by_well_id(db: Session, well_id: int) -> List[ChannelData]:
        return db.query(ChannelData).filter(ChannelData.well_id == well_id).all()

    @staticmethod
    def create_channel(db: Session, channel: ChannelDataCreate) -> ChannelData:
        # First check if well exists
        well = db.query(Well).filter(Well.id == channel.well_id).first()
        if not well:
            raise ValueError(f"Well with ID {channel.well_id} does not exist")
            
        # Check if channel already exists for this well
        existing_channel = ChannelDataRepository.get_channel_by_well_and_name(
            db, channel.well_id, channel.name
        )
        if existing_channel:
            raise ValueError(f"Channel '{channel.name}' already exists for well ID {channel.well_id}")
        
        # Create the channel
        db_channel = ChannelData(
            well_id=channel.well_id,
            name=channel.name,
            data_from=channel.data_from,
            data_to=channel.data_to
        )
        db.add(db_channel)
        db.commit()
        db.refresh(db_channel)
        
        # Now we can generate and return the bucket name
        return db_channel

    @staticmethod
    def update_channel(db: Session, channel_id: int, channel_update: ChannelDataUpdate) -> Optional[ChannelData]:
        db_channel = ChannelDataRepository.get_channel_by_id(db, channel_id)
        if not db_channel:
            return None
            
        update_data = channel_update.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_channel, field, value)
            
        db.commit()
        db.refresh(db_channel)
        return db_channel

    @staticmethod
    def delete_channel(db: Session, channel_id: int) -> bool:
        db_channel = ChannelDataRepository.get_channel_by_id(db, channel_id)
        if not db_channel:
            return False
            
        db.delete(db_channel)
        db.commit()
        return True