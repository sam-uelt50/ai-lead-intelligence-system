# backend/models/lead.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from .company import Company

class LeadResponse(BaseModel):
    company: Company
    score: int = Field(ge=0, le=100)
    priority: str
    reason: str
    next_best_action: str
    estimated_conversion_probability: int = Field(ge=0, le=100)
    signals_count: int = 0
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class Lead(BaseModel):
    company_id: str
    status: str = "new"
    priority: str
    score: int = Field(ge=0, le=100)
    assigned_to: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)