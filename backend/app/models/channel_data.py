from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime # type: ignore
from sqlalchemy.orm import relationship # type: ignore

from app.core.database import Base

class ChannelData(Base):
    __tablename__ = "channel_data"

    id = Column(Integer, primary_key=True, index=True)
    well_id = Column(Integer, ForeignKey("wells.id"), nullable=False)
    name = Column(String, nullable=False)
    data_from = Column(DateTime, nullable=False)
    data_to = Column(DateTime, nullable=True)  # Nullable if data collection is ongoing
    
   # Define the relationship back to Well
    well = relationship("Well", back_populates="channels")
    
    # Composite unique constraint for well_id + name
    __table_args__ = (
        # SQLAlchemy UniqueConstraint
        {'sqlite_autoincrement': True},
    )

    def __repr__(self):
        return f"<ChannelData {self.name} for Well {self.well_id}>"
    
    @property
    def bucket_name(self):
        """Generate the bucket name for this channel"""
        # This will require the well name, so we need to load the well
        # This assumes the well relationship is already loaded
        if self.well:
            return f"{self.well.name}_{self.name}"
        return f"unknown_well_{self.name}"