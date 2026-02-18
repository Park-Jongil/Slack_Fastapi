from pydantic import BaseModel, Field
from typing import Optional

class TeamDataResponse(BaseModel):
    id: int
    team_id: str
    name: str
    status: Optional[str] = None
    date: Optional[str] = None

    class Config:
        from_attributes = True

class StatisticsResponse(BaseModel):
    total_count: int
    
    class Config:
        extra = "allow"

class AlarmStatisticsResponse(BaseModel):
    Alarm: str
    Region: str
    NodeName: Optional[str] = None
    cnt: int

    class Config:
        from_attributes = True
