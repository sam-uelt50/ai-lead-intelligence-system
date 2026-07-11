# backend/models/company.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class SignalType(str, Enum):
    HIRING = "hiring"
    FUNDING = "funding"
    TECH_REFRESH = "tech_refresh"
    EXPANSION = "expansion"
    LEADERSHIP_CHANGE = "leadership_change"

class DecisionMaker(BaseModel):
    name: str
    title: str
    email: Optional[str] = None
    linkedin: Optional[str] = None
    role_category: Optional[str] = None  # "founder", "cmo", "marketing_director"
    decision_power: int = Field(default=50, ge=0, le=100)

class Company(BaseModel):
    name: str
    website: Optional[str] = None
    size: Optional[str] = None
    industry: Optional[str] = None
    growth_signals: List[dict] = Field(default_factory=list)  # Changed from [None]
    score: int = Field(default=0, ge=0, le=100)
    priority: str = Field(default="cold")  # "hot", "warm", "cold"
    research_brief: Optional[str] = None
    decision_makers: List[DecisionMaker] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }