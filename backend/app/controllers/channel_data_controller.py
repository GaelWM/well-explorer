from typing import List, Optional
from sqlalchemy.orm import Session # type: ignore
from fastapi import HTTPException # type: ignore

from app.repositories.channel_data_repository import ChannelDataRepository
from app.repositories.well_repository import WellRepository
from app.schemas.channel_data_schema import ChannelData, ChannelDataCreate, ChannelDataUpdate

class ChannelDataController:
    @staticmethod
    def get_channels(db: Session, skip: int = 0, limit: int = 100) -> List[ChannelData]:
        return ChannelDataRepository.get_channels(db, skip, limit)

    @staticmethod
    def get_channel_by_id(db: Session, channel_id: int) -> ChannelData:
        db_channel = ChannelDataRepository.get_channel_by_id(db, channel_id)
        if not db_channel:
            raise HTTPException(status_code=404, detail=f"Channel with id {channel_id} not found")
        return db_channel

    @staticmethod
    def get_channels_by_well_id(db: Session, well_id: int) -> List[ChannelData]:
        # Check if well exists
        well = WellRepository.get_well_by_id(db, well_id)
        if not well:
            raise HTTPException(status_code=404, detail=f"Well with id {well_id} not found")
        
        return ChannelDataRepository.get_channels_by_well_id(db, well_id)

    @staticmethod
    def create_channel(db: Session, channel: ChannelDataCreate) -> ChannelData:
        try:
            # Check if well exists first
            well = WellRepository.get_well_by_id(db, channel.well_id)
            if not well:
                raise HTTPException(status_code=404, detail=f"Well with id {channel.well_id} not found")
                
            return ChannelDataRepository.create_channel(db, channel)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def update_channel(db: Session, channel_id: int, channel_update: ChannelDataUpdate) -> ChannelData:
        db_channel = ChannelDataRepository.update_channel(db, channel_id, channel_update)
        if not db_channel:
            raise HTTPException(status_code=404, detail=f"Channel with id {channel_id} not found")
        return db_channel

    @staticmethod
    def delete_channel(db: Session, channel_id: int) -> dict:
        success = ChannelDataRepository.delete_channel(db, channel_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Channel with id {channel_id} not found")
        return {"message": f"Channel with id {channel_id} deleted successfully"}
    
    @staticmethod
    def get_channel_by_well_and_name(db: Session, well_id: int, name: str) -> ChannelData:
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
        return db_channel