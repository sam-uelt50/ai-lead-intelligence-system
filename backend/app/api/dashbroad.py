from fastapi import APIRouter, Query
from datetime import datetime, timedelta
from typing import Optional
from app.database import db

router = APIRouter()

@router.get("/dashboard/summary")
async def get_dashboard_summary():
    """Get dashboard overview"""
    try:
        # Count totals
        total_companies = db.companies.count_documents({})
        total_signals = db.signals.count_documents({})
        
        # Companies by priority
        priority_counts = {}
        for priority in ["hot", "warm", "cold"]:
            count = db.companies.count_documents({"priority": priority})
            priority_counts[priority] = count
        
        # Recent signals (last 7 days)
        week_ago = datetime.now() - timedelta(days=7)
        recent_signals = db.signals.count_documents({
            "detected_at": {"$gte": week_ago.isoformat()}
        })
        
        # Top companies by score
        top_companies = list(db.companies.find(
            {},
            {"_id": 0, "name": 1, "score": 1, "priority": 1, "signal_count": 1, "industry": 1}
        ).sort("score", -1).limit(5))
        
        return {
            "overview": {
                "total_companies": total_companies,
                "total_signals": total_signals,
                "recent_signals_7d": recent_signals
            },
            "priority_distribution": priority_counts,
            "top_companies": top_companies,
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}

@router.get("/companies")
async def get_companies(
    limit: int = Query(10, description="Number of companies"),
    priority: Optional[str] = Query(None, description="Filter by priority")
):
    """Get companies list"""
    query = {}
    if priority:
        query["priority"] = priority
    
    companies = list(db.companies.find(
        query,
        {"_id": 0, "name": 1, "industry": 1, "score": 1, "priority": 1, "signal_count": 1}
    ).limit(limit))
    
    return {"companies": companies, "count": len(companies)}

@router.get("/signals")
async def get_signals(limit: int = Query(10, description="Number of signals")):
    """Get recent signals"""
    signals = list(db.signals.find(
        {},
        {"_id": 0, "company_name": 1, "signal_type": 1, "description": 1, "detected_at": 1, "impact_score": 1}
    ).sort("detected_at", -1).limit(limit))
    
    return {"signals": signals, "count": len(signals)}