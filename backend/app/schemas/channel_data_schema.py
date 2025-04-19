from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field # type: ignore

# Shared properties
class ChannelDataBase(BaseModel):
    name: str = Field(..., description="Name of the channel data", min_length=1)
    data_from: Optional[datetime] = Field(None, description="Start date of the data range")
    data_to: Optional[datetime] = Field(None, description="End date of the data range")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation date of the channel data")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update date of the channel data")

# Properties to receive on ChannelData creation
class ChannelDataCreate(ChannelDataBase):
    well_id: int

# Properties to receive on ChannelData update
class ChannelDataUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Name of the channel data", min_length=1)
    data_from: Optional[datetime] = Field(None, description="Start date of the data range")
    data_to: Optional[datetime] = Field(None, description="End date of the data range")
    created_at: Optional[datetime] = Field(None, description="Creation date of the channel data")
    updated_at: Optional[datetime] = Field(None, description="Last update date of the channel data")

# Properties shared by models stored in DB
class ChannelDataInDBBase(ChannelDataBase):
    id: int
    well_id: int
    
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

# Properties to return to client
class ChannelData(ChannelDataInDBBase):
    pass

# Properties to return to client with extra fields
class ChannelDataExtended(ChannelData):
    bucket_name: str
    
# Properties stored in DB
class ChannelDataInDB(ChannelDataInDBBase):
    pass

# For nesting in Well responses
class ChannelDataSummary(BaseModel):
    id: int
    name: str
    data_from: Optional[datetime] = None
    data_to: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)