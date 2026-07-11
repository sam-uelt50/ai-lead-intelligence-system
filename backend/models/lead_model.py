from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class LeadStatus(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    CONVERTED = "converted"
    CLOSED = "closed"

class LeadSource(str, Enum):
    WEB_SCRAPE = "web_scrape"
    MANUAL_ENTRY = "manual_entry"
    IMPORT = "import"
    API = "api"

class LeadBase(BaseModel):
    name: str
    company: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    industry: Optional[str] = None
    tags: List[str] = []
    notes: Optional[str] = None
    source: LeadSource = LeadSource.WEB_SCRAPE
    status: LeadStatus = LeadStatus.NEW
    assigned_to: Optional[str] = None
    priority: int = Field(default=1, ge=1, le=5)

class LeadCreate(LeadBase):
    pass

class Lead(LeadBase):
    id: str = Field(alias="_id")
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }