from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import func, inspect # type: ignore

from app.models.bucket import get_bucket_model
from app.models.channel_data import ChannelData
from app.models.well import Well
from app.schemas.channel_data_schema import BucketDataCreate, BucketDataBatch

class BucketRepository:
    @staticmethod
    def get_data_points(
        db: Session, 
        well_name: str,
        channel_name: str,
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None,
        skip: int = 0, 
        limit: int = 1000
    ) -> List[Dict[str, Any]]:
        """Get time series data from a bucket for a specific well and channel"""
        # Get the dynamic model for this bucket
        BucketModel = get_bucket_model(well_name, channel_name)
        
        # Build the query
        query = db.query(BucketModel)
        
        if start_date:
            query = query.filter(BucketModel.time >= start_date)
        if end_date:
            query = query.filter(BucketModel.time <= end_date)
            
        # Execute the query with pagination
        results = query.order_by(BucketModel.time).offset(skip).limit(limit).all()
        
        # Convert to dictionaries for easier serialization
        return [{"id": item.id, "time": item.time, "value": item.value} for item in results]

    @staticmethod
    def create_data_point(
        db: Session, 
        well_name: str,
        channel_name: str,
        data_point: BucketDataCreate
    ) -> Dict[str, Any]:
        """Create a new data point in a bucket for a specific well and channel"""
        # Get the dynamic model for this bucket
        BucketModel = get_bucket_model(well_name, channel_name)
        
        # Create the data point
        db_data_point = BucketModel(
            time=data_point.time,
            value=data_point.value
        )
        db.add(db_data_point)
        
        # Find the channel to update its data_from and data_to
        channel = db.query(ChannelData).join(Well).filter(
            Well.name == well_name,
            ChannelData.name == channel_name
        ).first()
        
        if channel:
            # Update channel data_to if needed
            if not channel.data_to or data_point.time > channel.data_to:
                channel.data_to = data_point.time
            # Update channel data_from if needed
            if not channel.data_from or data_point.time < channel.data_from:
                channel.data_from = data_point.time
        
        db.commit()
        db.refresh(db_data_point)
        
        # Convert to dictionary for serialization
        return {
            "id": db_data_point.id,
            "time": db_data_point.time,
            "value": db_data_point.value
        }

    @staticmethod
    def create_data_points_batch(
        db: Session, 
        well_name: str,
        channel_name: str,
        data_points: BucketDataBatch
    ) -> List[Dict[str, Any]]:
        """Create multiple data points in a bucket for a specific well and channel"""
        # Get the dynamic model for this bucket
        BucketModel = get_bucket_model(well_name, channel_name)
        
        # Find the channel to update its data_from and data_to
        channel = db.query(ChannelData).join(Well).filter(
            Well.name == well_name,
            ChannelData.name == channel_name
        ).first()
        
        # Track earliest and latest times
        earliest_time = None
        latest_time = None
        
        # Create all data points
        db_data_points = []
        for data_point in data_points.data_points:
            point = BucketModel(
                time=data_point.time,
                value=data_point.value
            )
            db.add(point)
            db_data_points.append(point)
            
            # Track earliest and latest times
            if earliest_time is None or data_point.time < earliest_time:
                earliest_time = data_point.time
            if latest_time is None or data_point.time > latest_time:
                latest_time = data_point.time
        
        # Update channel data_from and data_to if needed
        if channel and earliest_time:
            if not channel.data_from or earliest_time < channel.data_from:
                channel.data_from = earliest_time
        if channel and latest_time:
            if not channel.data_to or latest_time > channel.data_to:
                channel.data_to = latest_time
        
        db.commit()
        
        # Convert to dictionaries for serialization
        return [{"id": item.id, "time": item.time, "value": item.value} for item in db_data_points]

    @staticmethod
    def delete_data_point(
        db: Session, 
        well_name: str,
        channel_name: str,
        data_point_id: int
    ) -> bool:
        """Delete a specific data point from a bucket"""
        # Get the dynamic model for this bucket
        BucketModel = get_bucket_model(well_name, channel_name)
        
        # Find and delete the data point
        db_data_point = db.query(BucketModel).filter(BucketModel.id == data_point_id).first()
        if not db_data_point:
            return False
            
        db.delete(db_data_point)
        db.commit()
        return True
    
    @staticmethod
    def delete_all_bucket_data(
        db: Session, 
        well_name: str,
        channel_name: str
    ) -> int:
        """Delete all data points from a bucket and return the count of deleted rows"""
        # Get the dynamic model for this bucket
        BucketModel = get_bucket_model(well_name, channel_name)
        
        # Delete all data points
        result = db.query(BucketModel).delete()
        db.commit()
        return result
    
    @staticmethod
    def get_statistics(
        db: Session, 
        well_name: str,
        channel_name: str,
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get statistics for a bucket's data"""
        # Get the dynamic model for this bucket
        BucketModel = get_bucket_model(well_name, channel_name)
        
        # Build the query for statistics
        query = db.query(
            func.min(BucketModel.value).label("min"),
            func.max(BucketModel.value).label("max"),
            func.avg(BucketModel.value).label("avg"),
            func.count(BucketModel.id).label("count")
        )
        
        # Apply date filters if provided
        if start_date:
            query = query.filter(BucketModel.time >= start_date)
        if end_date:
            query = query.filter(BucketModel.time <= end_date)
            
        # Execute the query
        result = query.first()
        
        # Return the statistics
        return {
            "min": result.min,
            "max": result.max,
            "avg": result.avg,
            "count": result.count
        }