from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session # type: ignore
from fastapi import HTTPException # type: ignore

from app.repositories.bucket_repository import BucketRepository
from app.repositories.channel_data_repository import ChannelDataRepository
from app.repositories.well_repository import WellRepository
from app.schemas.bucket_schema import BucketDataCreate, BucketDataBatch, BucketDataOut, BucketStatistics

class BucketController:
    @staticmethod
    def get_data_points(
        db: Session, 
        well_name: str,
        channel_name: str,
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None,
        skip: int = 0, 
        limit: int = 1000
    ) -> List[BucketDataOut]:
        """Get time series data from a bucket for a specific well and channel"""
        # Check if well and channel exist
        well = WellRepository.get_well_by_name(db, well_name)
        if not well:
            raise HTTPException(status_code=404, detail=f"Well with name '{well_name}' not found")
        
        channel = ChannelDataRepository.get_channel_by_well_and_name(db, well.id, channel_name)
        if not channel:
            raise HTTPException(
                status_code=404, 
                detail=f"Channel with name '{channel_name}' not found for well '{well_name}'"
            )
        
        # Get the data points
        data_points = BucketRepository.get_data_points(
            db, well_name, channel_name, start_date, end_date, skip, limit
        )
        
        return [BucketDataOut(**point) for point in data_points]

    @staticmethod
    def create_data_point(
        db: Session, 
        well_name: str,
        channel_name: str,
        data_point: BucketDataCreate
    ) -> BucketDataOut:
        """Create a new data point in a bucket for a specific well and channel"""
        # Check if well and channel exist
        well = WellRepository.get_well_by_name(db, well_name)
        if not well:
            raise HTTPException(status_code=404, detail=f"Well with name '{well_name}' not found")
        
        channel = ChannelDataRepository.get_channel_by_well_and_name(db, well.id, channel_name)
        if not channel:
            raise HTTPException(
                status_code=404, 
                detail=f"Channel with name '{channel_name}' not found for well '{well_name}'"
            )
        
        # Create the data point
        result = BucketRepository.create_data_point(db, well_name, channel_name, data_point)
        
        return BucketDataOut(**result)

    @staticmethod
    def create_data_points_batch(
        db: Session, 
        well_name: str,
        channel_name: str,
        data_points: BucketDataBatch
    ) -> List[BucketDataOut]:
        """Create multiple data points in a bucket for a specific well and channel"""
        # Check if well and channel exist
        well = WellRepository.get_well_by_name(db, well_name)
        if not well:
            raise HTTPException(status_code=404, detail=f"Well with name '{well_name}' not found")
        
        channel = ChannelDataRepository.get_channel_by_well_and_name(db, well.id, channel_name)
        if not channel:
            raise HTTPException(
                status_code=404, 
                detail=f"Channel with name '{channel_name}' not found for well '{well_name}'"
            )
        
        # Create the data points
        results = BucketRepository.create_data_points_batch(db, well_name, channel_name, data_points)
        
        return [BucketDataOut(**point) for point in results]

    @staticmethod
    def delete_data_point(
        db: Session, 
        well_name: str,
        channel_name: str,
        data_point_id: int
    ) -> Dict[str, str]:
        """Delete a specific data point from a bucket"""
        # Check if well and channel exist
        well = WellRepository.get_well_by_name(db, well_name)
        if not well:
            raise HTTPException(status_code=404, detail=f"Well with name '{well_name}' not found")
        
        channel = ChannelDataRepository.get_channel_by_well_and_name(db, well.id, channel_name)
        if not channel:
            raise HTTPException(
                status_code=404, 
                detail=f"Channel with name '{channel_name}' not found for well '{well_name}'"
            )
        
        # Delete the data point
        success = BucketRepository.delete_data_point(db, well_name, channel_name, data_point_id)
        if not success:
            raise HTTPException(
                status_code=404, 
                detail=f"Data point with id {data_point_id} not found in bucket '{well_name}_{channel_name}'"
            )
        
        return {"message": f"Data point with id {data_point_id} deleted successfully"}
    
    @staticmethod
    def delete_all_bucket_data(
        db: Session, 
        well_name: str,
        channel_name: str
    ) -> Dict[str, str]:
        """Delete all data points from a bucket"""
        # Check if well and channel exist
        well = WellRepository.get_well_by_name(db, well_name)
        if not well:
            raise HTTPException(status_code=404, detail=f"Well with name '{well_name}' not found")
        
        channel = ChannelDataRepository.get_channel_by_well_and_name(db, well.id, channel_name)
        if not channel:
            raise HTTPException(
                status_code=404, 
                detail=f"Channel with name '{channel_name}' not found for well '{well_name}'"
            )
        
        # Delete all data points
        count = BucketRepository.delete_all_bucket_data(db, well_name, channel_name)
        
        return {"message": f"Deleted {count} data points from bucket '{well_name}_{channel_name}'"}
    
    @staticmethod
    def get_statistics(
        db: Session, 
        well_name: str,
        channel_name: str,
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None
    ) -> BucketStatistics:
        """Get statistics for a bucket's data"""
        # Check if well and channel exist
        well = WellRepository.get_well_by_name(db, well_name)
        if not well:
            raise HTTPException(status_code=404, detail=f"Well with name '{well_name}' not found")
        
        channel = ChannelDataRepository.get_channel_by_well_and_name(db, well.id, channel_name)
        if not channel:
            raise HTTPException(
                status_code=404, 
                detail=f"Channel with name '{channel_name}' not found for well '{well_name}'"
            )
        
        # Get the statistics
        stats = BucketRepository.get_statistics(db, well_name, channel_name, start_date, end_date)
        
        if stats["count"] == 0:
            raise HTTPException(
                status_code=404, 
                detail=f"No data points found in bucket '{well_name}_{channel_name}' for the specified time range"
            )
        
        return BucketStatistics(**stats)