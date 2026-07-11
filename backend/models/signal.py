# backend/models/signal.py
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any

class SignalType(str, Enum):
    HIRING = "hiring"
    FUNDING = "funding"
    TECH_REFRESH = "tech_refresh"
    EXPANSION = "expansion"
    LEADERSHIP_CHANGE = "leadership_change"
    PRODUCT_LAUNCH = "product_launch"
    PARTNERSHIP = "partnership"

class Signal(BaseModel):
    type: SignalType
    description: str
    confidence: int = Field(ge=0, le=100)
    source: str
    detected_at: datetime = Field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = None
    company_id: Optional[str] = None