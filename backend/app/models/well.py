from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Date # type: ignore
from sqlalchemy.orm import relationship # type: ignore

from app.core.database import Base

class Well(Base):
    __tablename__ = "wells"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    lift_type = Column(String, nullable=True)
    region = Column(String, nullable=False)
    installation_date = Column(Date, nullable=True)
    depth = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.today)
    updated_at = Column(DateTime, nullable=False, default=datetime.today, onupdate=date.today)
    
    # Define the relationship with ChannelData
    channels = relationship("ChannelData", back_populates="well", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Well {self.name}>"