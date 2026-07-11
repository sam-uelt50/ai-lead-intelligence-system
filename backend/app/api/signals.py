from fastapi import APIRouter, Query
from datetime import datetime, timedelta
from typing import Optional
from app.database import db

router = APIRouter()

@router.get("/signals")
async def get_signals(
    skip: int = Query(0, description="Skip records"),
    limit: int = Query(50, description="Limit records"),
    category: Optional[str] = Query(None, description="Filter by category"),
    signal_type: Optional[str] = Query(None, description="Filter by signal type"),
    company_name: Optional[str] = Query(None, description="Filter by company"),
    days: Optional[int] = Query(None, description="Last N days")
):
    """Get signals with optional filtering"""
    
    query = {}
    
    if category:
        query["category"] = category
    if signal_type:
        query["signal_type"] = signal_type
    if company_name:
        query["company_name"] = company_name
    if days:
        start_date = datetime.utcnow() - timedelta(days=days)
        query["detected_at"] = {"$gte": start_date.isoformat()}
    
    signals = list(db.signals.find(
        query,
        {"_id": 0}
    ).sort("detected_at", -1).skip(skip).limit(limit))
    
    total = db.signals.count_documents(query)
    
    return {
        "signals": signals,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@router.get("/signals/recent")
async def get_recent_signals(limit: int = Query(10, description="Number of recent signals")):
    """Get most recent signals"""
    
    signals = list(db.signals.find(
        {},
        {
            "_id": 0,
            "signal_type": 1,
            "company_name": 1,
            "description": 1,
            "detected_at": 1,
            "impact_score": 1,
            "category": 1,
            "source": 1
        }
    ).sort("detected_at", -1).limit(limit))
    
    return {"recent_signals": signals}