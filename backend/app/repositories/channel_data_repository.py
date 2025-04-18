from typing import List, Optional, Tuple
from datetime import datetime
from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import func, desc # type: ignore

from app.models.channel_data import ChannelData
from app.models.well import Well
from app.schemas.channel_data_schema import ChannelDataCreate, ChannelDataUpdate
from app.models.bucket import get_bucket_model

class ChannelDataRepository:
    @staticmethod
    def get_channels(db: Session, skip: int = 0, limit: int = 100) -> List[ChannelData]:
        """Get all channels with pagination"""
        return db.query(ChannelData).offset(skip).limit(limit).all()

    @staticmethod
    def get_channel_by_id(db: Session, channel_id: int) -> Optional[ChannelData]:
        """Get a channel by its ID"""
        return db.query(ChannelData).filter(ChannelData.id == channel_id).first()

    @staticmethod
    def get_channels_by_well_id(db: Session, well_id: int) -> List[ChannelData]:
        """Get all channels for a specific well"""
        return db.query(ChannelData).filter(ChannelData.well_id == well_id).all()
    
    @staticmethod
    def get_channel_by_well_and_name(db: Session, well_id: int, name: str) -> Optional[ChannelData]:
        """Get a channel by well ID and channel name"""
        return db.query(ChannelData).filter(
            ChannelData.well_id == well_id,
            ChannelData.name == name
        ).first()
        
    @staticmethod
    def get_channel_by_well_name_and_channel_name(
        db: Session, well_name: str, channel_name: str
    ) -> Optional[ChannelData]:
        """Get a channel by well name and channel name"""
        return db.query(ChannelData).join(Well).filter(
            Well.name == well_name,
            ChannelData.name == channel_name
        ).first()

    @staticmethod
    def create_channel(db: Session, channel: ChannelDataCreate) -> ChannelData:
        """Create a new channel for a well"""
        # Check if well exists
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
        
        # Create the bucket table for this channel
        # This ensures the table exists when data is added
        get_bucket_model(well.name, channel.name)
        
        return db_channel

    @staticmethod
    def update_channel(db: Session, channel_id: int, channel_update: ChannelDataUpdate) -> Optional[ChannelData]:
        """Update an existing channel"""
        db_channel = ChannelDataRepository.get_channel_by_id(db, channel_id)
        if not db_channel:
            return None
        
        # If name is changing, need to handle bucket name change
        if channel_update.name is not None and channel_update.name != db_channel.name:
            # Check if the new name already exists for this well
            existing_channel = ChannelDataRepository.get_channel_by_well_and_name(
                db, db_channel.well_id, channel_update.name
            )
            if existing_channel:
                raise ValueError(
                    f"Channel '{channel_update.name}' already exists for well ID {db_channel.well_id}"
                )
            
            # TODO: Handle renaming the bucket table if needed
            # This would require database migration logic
        
        update_data = channel_update.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_channel, field, value)
            
        db.commit()
        db.refresh(db_channel)
        return db_channel

    @staticmethod
    def delete_channel(db: Session, channel_id: int) -> bool:
        """Delete a channel (note: this does not delete the bucket data)"""
        db_channel = ChannelDataRepository.get_channel_by_id(db, channel_id)
        if not db_channel:
            return False
        
        # TODO: Consider whether to delete the bucket data table
        # This would require additional logic with the bucket factory
            
        db.delete(db_channel)
        db.commit()
        return True
    
    @staticmethod
    def update_channel_time_range(
        db: Session, channel_id: int, time_point: datetime
    ) -> Optional[ChannelData]:
        """Update a channel's data_from and data_to based on new data point"""
        db_channel = ChannelDataRepository.get_channel_by_id(db, channel_id)
        if not db_channel:
            return None
        
        if db_channel.data_from is None or time_point < db_channel.data_from:
            db_channel.data_from = time_point
        
        if db_channel.data_to is None or time_point > db_channel.data_to:
            db_channel.data_to = time_point
        
        db.commit()
        db.refresh(db_channel)
        return db_channel
    
    @staticmethod
    def get_channel_count_by_well_id(db: Session, well_id: int) -> int:
        """Get the count of channels for a specific well"""
        return db.query(func.count(ChannelData.id)).filter(ChannelData.well_id == well_id).scalar()