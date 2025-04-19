import datetime
import random
import math
from typing import Optional, List, Dict, Any, Union
from sqlalchemy.orm import Session # type: ignore

from app.models.bucket import get_bucket_model
from app.repositories.channel_data_repository import ChannelDataRepository
from app.repositories.well_repository import WellRepository

class BucketDataGenerator:
    @staticmethod
    def populate_bucket(
        db: Session,
        well_name: str,
        channel_name: str,
        start_date: Optional[datetime.datetime] = None,
        end_date: Optional[datetime.datetime] = None,
        interval_seconds: int = 3600,  # Default: hourly
        value_generator: Optional[callable] = None,
        update_channel_dates: bool = True
    ) -> Dict[str, Any]:
        """
        Populate a bucket with time series data points at regular intervals.
        
        Args:
            db: Database session
            well_name: Name of the well
            channel_name: Name of the channel
            start_date: Start date for data generation (defaults to channel's data_from or current date - 30 days)
            end_date: End date for data generation (defaults to channel's data_to or current date)
            interval_seconds: Time interval between data points in seconds
            value_generator: Function to generate values, receives timestamp as input. Defaults to sine wave + random noise
            update_channel_dates: Whether to update the channel's data_from and data_to dates
            
        Returns:
            Dict with information about the generated data
        """
        # Check if well and channel exist
        well = WellRepository.get_well_by_name(db, well_name)
        if not well:
            raise ValueError(f"Well with name '{well_name}' not found")
        
        channel = ChannelDataRepository.get_channel_by_well_and_name(db, well.id, channel_name)
        if not channel:
            raise ValueError(f"Channel with name '{channel_name}' not found for well '{well_name}'")
        
        # Determine date range
        now = datetime.datetime.now()
        
        if not start_date:
            start_date = channel.data_from if channel.data_from else now - datetime.timedelta(days=30)
        
        if not end_date:
            end_date = channel.data_to if channel.data_to else now
        
        # Ensure start_date is before end_date
        if start_date >= end_date:
            raise ValueError(f"Start date ({start_date}) must be before end date ({end_date})")
        
        # Use default value generator if none provided
        if not value_generator:
            def default_value_generator(timestamp):
                # Generate a value based on sine wave + random noise
                # This creates realistic-looking time series data
                days_since_start = (timestamp - start_date).total_seconds() / 86400
                base_value = 50 + 25 * math.sin(days_since_start * math.pi / 15)  # Sine wave with 30-day period
                noise = random.uniform(-5, 5)  # Random noise
                return round(base_value + noise, 2)
            
            value_generator = default_value_generator
        
        # Get the bucket model
        BucketModel = get_bucket_model(well_name, channel_name)
        
        # Generate data points
        current_time = start_date
        points_generated = 0
        earliest_time = None
        latest_time = None
        
        while current_time <= end_date:
            # Generate a value for this timestamp
            value = value_generator(current_time)
            
            # Create the data point
            db_point = BucketModel(
                time=current_time,
                value=value
            )
            db.add(db_point)
            
            # Track earliest and latest times
            if earliest_time is None or current_time < earliest_time:
                earliest_time = current_time
            if latest_time is None or current_time > latest_time:
                latest_time = current_time
            
            # Move to the next time
            current_time += datetime.timedelta(seconds=interval_seconds)
            points_generated += 1
        
        # Update channel's date range if needed
        if update_channel_dates:
            if channel.data_from is None or earliest_time < channel.data_from:
                channel.data_from = earliest_time
            if channel.data_to is None or latest_time > channel.data_to:
                channel.data_to = latest_time
        
        # Commit all changes
        db.commit()
        
        return {
            "well_name": well_name,
            "channel_name": channel_name,
            "points_generated": points_generated,
            "start_date": start_date,
            "end_date": end_date,
            "interval_seconds": interval_seconds
        }
    
    @staticmethod
    def generate_pattern_data(
        db: Session,
        well_name: str,
        channel_name: str,
        pattern_type: str = "sine",
        start_date: Optional[datetime.datetime] = None,
        end_date: Optional[datetime.datetime] = None,
        interval_seconds: int = 3600,
        base_value: float = 50.0,
        amplitude: float = 25.0,
        period_days: float = 7.0,
        trend_slope: float = 0.0,
        noise_level: float = 2.0
    ) -> Dict[str, Any]:
        """
        Generate time series data with specific patterns.
        
        Args:
            db: Database session
            well_name: Name of the well
            channel_name: Name of the channel
            pattern_type: Type of pattern ('sine', 'cosine', 'sawtooth', 'square', 'random', 'trend')
            start_date: Start date for data generation
            end_date: End date for data generation
            interval_seconds: Time interval between data points in seconds
            base_value: Base value for the generated data
            amplitude: Amplitude of the pattern variation
            period_days: Period of the pattern in days
            trend_slope: Slope of the trend (units per day)
            noise_level: Magnitude of random noise to add
            
        Returns:
            Dict with information about the generated data
        """
        def create_generator(pattern_type):
            def value_generator(timestamp):
                days_since_start = (timestamp - start_date).total_seconds() / 86400
                
                # Add trend component if specified
                trend = trend_slope * days_since_start
                
                # Generate the pattern value
                if pattern_type == "sine":
                    pattern = amplitude * math.sin(2 * math.pi * days_since_start / period_days)
                elif pattern_type == "cosine":
                    pattern = amplitude * math.cos(2 * math.pi * days_since_start / period_days)
                elif pattern_type == "sawtooth":
                    pattern = amplitude * (2 * (days_since_start / period_days - math.floor(0.5 + days_since_start / period_days)))
                elif pattern_type == "square":
                    pattern = amplitude if math.sin(2 * math.pi * days_since_start / period_days) >= 0 else -amplitude
                elif pattern_type == "random":
                    pattern = 0  # Pure noise
                elif pattern_type == "trend":
                    pattern = 0  # Pure trend
                else:
                    pattern = 0
                
                # Add random noise
                noise = random.uniform(-noise_level, noise_level)
                
                # Combine all components
                return round(base_value + pattern + trend + noise, 2)
            
            return value_generator
        
        # Use the pattern-specific generator
        return BucketDataGenerator.populate_bucket(
            db=db,
            well_name=well_name,
            channel_name=channel_name,
            start_date=start_date,
            end_date=end_date,
            interval_seconds=interval_seconds,
            value_generator=create_generator(pattern_type)
        )