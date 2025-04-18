from typing import List, Dict
from sqlalchemy.orm import Session # type: ignore
from fastapi import HTTPException # type: ignore

from app.repositories.channel_data_repository import ChannelDataRepository
from app.repositories.well_repository import WellRepository
from app.schemas.channel_data_schema import (
    ChannelData, 
    ChannelDataCreate, 
    ChannelDataUpdate,
    ChannelDataExtended
)

class ChannelDataController:
    @staticmethod
    def get_channels(db: Session, skip: int = 0, limit: int = 100) -> List[ChannelData]:
        """Get all channels with pagination"""
        return ChannelDataRepository.get_channels(db, skip, limit)

    @staticmethod
    def get_channel_by_id(db: Session, channel_id: int) -> ChannelDataExtended:
        """Get a channel by its ID with extended info including bucket name"""
        db_channel = ChannelDataRepository.get_channel_by_id(db, channel_id)
        if not db_channel:
            raise HTTPException(status_code=404, detail=f"Channel with id {channel_id} not found")
        
        # Convert to ChannelDataExtended
        channel_data = ChannelData.from_orm(db_channel)
        channel_extended = ChannelDataExtended(
            **channel_data.dict(),
            bucket_name=db_channel.bucket_name
        )
        
        return channel_extended

    @staticmethod
    def get_channels_by_well_id(db: Session, well_id: int) -> List[ChannelData]:
        """Get all channels for a specific well"""
        # Check if well exists
        well = WellRepository.get_well_by_id(db, well_id)
        if not well:
            raise HTTPException(status_code=404, detail=f"Well with id {well_id} not found")
        
        return ChannelDataRepository.get_channels_by_well_id(db, well_id)

    @staticmethod
    def create_channel(db: Session, channel: ChannelDataCreate) -> ChannelDataExtended:
        """Create a new channel for a well with extended info including bucket name"""
        try:
            # Check if well exists first
            well = WellRepository.get_well_by_id(db, channel.well_id)
            if not well:
                raise HTTPException(status_code=404, detail=f"Well with id {channel.well_id} not found")
                
            db_channel = ChannelDataRepository.create_channel(db, channel)
            
            # Convert to ChannelDataExtended
            channel_data = ChannelData.from_orm(db_channel)
            channel_extended = ChannelDataExtended(
                **channel_data.dict(),
                bucket_name=db_channel.bucket_name
            )
            
            return channel_extended
            
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def update_channel(db: Session, channel_id: int, channel_update: ChannelDataUpdate) -> ChannelDataExtended:
        """Update an existing channel with extended info including bucket name"""
        try:
            db_channel = ChannelDataRepository.update_channel(db, channel_id, channel_update)
            if not db_channel:
                raise HTTPException(status_code=404, detail=f"Channel with id {channel_id} not found")
            
            # Convert to ChannelDataExtended
            channel_data = ChannelData.from_orm(db_channel)
            channel_extended = ChannelDataExtended(
                **channel_data.dict(),
                bucket_name=db_channel.bucket_name
            )
            
            return channel_extended
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def delete_channel(db: Session, channel_id: int) -> Dict[str, str]:
        """Delete a channel"""
        success = ChannelDataRepository.delete_channel(db, channel_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Channel with id {channel_id} not found")
        return {"message": f"Channel with id {channel_id} deleted successfully"}
    
    @staticmethod
    def get_channel_by_well_and_name(db: Session, well_id: int, name: str) -> ChannelDataExtended:
        """Get a channel by well ID and channel name with extended info including bucket name"""
        # Check if well exists
        well = WellRepository.get_well_by_id(db, well_id)
        if not well:
            raise HTTPException(status_code=404, detail=f"Well with id {well_id} not found")
            
        db_channel = ChannelDataRepository.get_channel_by_well_and_name(db, well_id, name)
        if not db_channel:
            raise HTTPException(
                status_code=404, 
                detail=f"Channel with name '{name}' not found for well with id {well_id}"
            )
        
        # Convert to ChannelDataExtended
        channel_data = ChannelData.from_orm(db_channel)
        channel_extended = ChannelDataExtended(
            **channel_data.dict(),
            bucket_name=db_channel.bucket_name
        )
        
        return channel_extended
    
    @staticmethod
    def get_channel_by_well_name_and_channel_name(
        db: Session, well_name: str, channel_name: str
    ) -> ChannelDataExtended:
        """Get a channel by well name and channel name with extended info including bucket name"""
        # Check if well exists
        well = WellRepository.get_well_by_name(db, well_name)
        if not well:
            raise HTTPException(status_code=404, detail=f"Well with name '{well_name}' not found")
            
        db_channel = ChannelDataRepository.get_channel_by_well_name_and_channel_name(
            db, well_name, channel_name
        )
        if not db_channel:
            raise HTTPException(
                status_code=404, 
                detail=f"Channel with name '{channel_name}' not found for well '{well_name}'"
            )
        
        # Convert to ChannelDataExtended
        channel_data = ChannelData.from_orm(db_channel)
        channel_extended = ChannelDataExtended(
            **channel_data.dict(),
            bucket_name=db_channel.bucket_name
        )
        
        return channel_extended