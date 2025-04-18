from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel # type: ignore

# Shared properties
class ChannelDataBase(BaseModel):
    name: str
    data_from: datetime
    data_to: Optional[datetime] = None

# Properties to receive on ChannelData creation
class ChannelDataCreate(ChannelDataBase):
    well_id: int

# Properties to receive on ChannelData update
class ChannelDataUpdate(BaseModel):
    name: Optional[str] = None
    data_from: Optional[datetime] = None
    data_to: Optional[datetime] = None

# Properties shared by models stored in DB
class ChannelDataInDBBase(ChannelDataBase):
    id: int
    well_id: int
    
    class Config:
        from_attributes = True

# Properties to return to client
class ChannelData(ChannelDataInDBBase):
    bucket_name: str
    
# Properties stored in DB
class ChannelDataInDB(ChannelDataInDBBase):
    pass