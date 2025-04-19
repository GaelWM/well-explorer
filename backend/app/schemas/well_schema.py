from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field, field_validator # type: ignore

# Import the Pydantic schema for ChannelData, not the SQLAlchemy model
from app.schemas.channel_data_schema import ChannelDataSummary

# Shared properties
class WellBase(BaseModel):
    name: str = Field(..., description="Name of the well", min_length=1)
    latitude: float = Field(..., description="Latitude in decimal")
    longitude: float = Field(..., description="Longitude in decimal")
    lift_type: Optional[str] = Field(None, description="Type of lift mechanism")
    region: str = Field(..., description="Region where the well is located", min_length=1)
    installation_date: Optional[date] = Field(None, description="Date when the well was installed")
    depth: Optional[float] = Field(None, description="Depth of the well in meters")
    status: Optional[str] = Field(None, description="Status of the well (e.g., active, inactive)")
    created_at: datetime = Field(default_factory=datetime.today, description="Creation date of the well")
    updated_at: datetime = Field(default_factory=datetime.today, description="Last update date of the well")
    
    @field_validator('name', 'region')
    @classmethod
    def validate_non_empty_string(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("This field cannot be empty")
        return v.strip()

# Properties to receive on well creation
class WellCreate(WellBase):
    pass

# Properties to receive on well update
class WellUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Name of the well", min_length=1)
    latitude: Optional[float] = Field(None, description="Latitude in decimal degrees", ge=-90, le=90)
    longitude: Optional[float] = Field(None, description="Longitude in decimal degrees", ge=-180, le=180)
    lift_type: Optional[str] = Field(None, description="Type of lift mechanism")
    region: Optional[str] = Field(None, description="Region where the well is located", min_length=1)
    installation_date: Optional[date] = Field(None, description="Date when the well was installed")
    depth: Optional[float] = Field(None, description="Depth of the well in meters")
    status: Optional[str] = Field(None, description="Status of the well (e.g., active, inactive)")
    created_at: Optional[datetime] = Field(None, description="Creation date of the well")
    updated_at: Optional[datetime] = Field(None, description="Last update date of the well")
    
    @field_validator('name', 'region')
    @classmethod
    def validate_non_empty_string(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not v.strip():
            raise ValueError("This field cannot be empty")
        return v.strip()

# Properties shared by models stored in DB
class WellInDBBase(WellBase):
    id: int

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

# Properties to return to client
class Well(WellInDBBase):
    pass

# Properties to return to client with nested channels
class WellWithChannels(WellInDBBase):
    channels: List[ChannelDataSummary] = []

# Properties stored in DB
class WellInDB(WellInDBBase):
    pass