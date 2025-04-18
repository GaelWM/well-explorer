from datetime import date
from typing import List, Optional
from app.models.channel_data import ChannelData
from pydantic import BaseModel, Field # type: ignore

# Shared properties
class WellBase(BaseModel):
    name: str
    latitude: float
    longitude: float
    lift_type: Optional[str] = None
    region: str
    installation_date: Optional[date] = None
    depth: Optional[float] = Field(None, gt=0, description="Depth of the well in meters")
    status: Optional[str] = Field(None, description="Status of the well (e.g., active, inactive)")

# Properties to receive on well creation
class WellCreate(WellBase):
    pass

# Properties to receive on well update
class WellUpdate(BaseModel):
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    lift_type: Optional[str] = None
    region: Optional[str] = None
    installation_date: Optional[date] = None
    depth: Optional[float] = Field(None, gt=0, description="Depth of the well in meters")
    status: Optional[str] = Field(None, description="Status of the well (e.g., active, inactive)")

# Properties shared by models stored in DB
class WellInDBBase(WellBase):
    id: int

    class Config:
        from_attributes = True

# Properties to return to client
class Well(WellInDBBase):
    pass

# Properties to return to client with nested channels
class WellWithChannels(WellInDBBase):
    channels: List[ChannelData] = []

# Properties stored in DB
class WellInDB(WellInDBBase):
    pass