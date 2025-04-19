from datetime import date, datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint, Date # type: ignore
from sqlalchemy.orm import relationship # type: ignore

from app.core.database import Base

class ChannelData(Base):
    __tablename__ = "channel_data"

    id = Column(Integer, primary_key=True, index=True)
    well_id = Column(Integer, ForeignKey("wells.id"), nullable=False)
    name = Column(String, nullable=False, index=True)
    data_from = Column(DateTime, nullable=True)  # Nullable until data is added
    data_to = Column(DateTime, nullable=True)    # Nullable until data is added
    created_at = Column(DateTime, nullable=False, default=datetime.today)
    updated_at = Column(DateTime, nullable=False, default=datetime.today, onupdate=date.today)
    
    # Define the relationship back to Well
    well = relationship("Well", back_populates="channels")
    
    # Ensure well_id + name combination is unique
    __table_args__ = (
        UniqueConstraint('well_id', 'name', name='uix_well_channel'),
    )

    def __repr__(self):
        return f"<ChannelData {self.name} for Well {self.well_id}>"
    
    @property
    def bucket_name(self):
        """Generate the bucket name for this channel"""
        # This will require the well name, so we need to load the well
        if self.well:
            return f"{self.well.name}_{self.name}"
        return f"unknown_well_{self.name}"
        
    @property
    def table_name(self):
        """Generate the database table name for this channel's bucket"""
        if self.well:
            # Create a valid table name from well_name and channel_name
            # Replace invalid chars with underscores and lowercase everything
            def sanitize_name(name):
                return ''.join(c.lower() if c.isalnum() else '_' for c in name)
            
            well_name_safe = sanitize_name(self.well.name)
            channel_name_safe = sanitize_name(self.name)
            
            return f"bucket_{well_name_safe}_{channel_name_safe}"
        return None