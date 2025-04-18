from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict # type: ignore

# Schema for a data point in a bucket
class BucketDataBase(BaseModel):
    time: datetime
    value: float

# Schema for creating a single data point
class BucketDataCreate(BucketDataBase):
    pass

# Schema for creating multiple data points in a batch
class BucketDataBatch(BaseModel):
    data_points: List[BucketDataBase]

# Schema for returning a data point from a bucket
class BucketDataOut(BucketDataBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

# Schema for statistics of a bucket
class BucketStatistics(BaseModel):
    min: Optional[float] = None
    max: Optional[float] = None
    avg: Optional[float] = None
    count: int