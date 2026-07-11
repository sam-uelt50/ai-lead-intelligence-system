from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.database import db

router = APIRouter()

@router.get("/companies")
async def get_companies(
    skip: int = Query(0, description="Skip records"),
    limit: int = Query(100, description="Limit records"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    industry: Optional[str] = Query(None, description="Filter by industry"),
    search: Optional[str] = Query(None, description="Search by company name")
):
    """Get companies with optional filtering"""
    
    query = {}
    
    if priority:
        query["priority"] = priority
    if industry:
        query["industry"] = industry
    if search:
        query["name"] = {"$regex": search, "$options": "i"}
    
    companies = list(db.companies.find(
        query,
        {
            "_id": 0,
            "name": 1,
            "industry": 1,
            "location": 1,
            "score": 1,
            "priority": 1,
            "signal_count": 1,
            "employee_count": 1,
            "decision_makers": 1,
            "last_signal_at": 1
        }
    ).skip(skip).limit(limit))
    
    total = db.companies.count_documents(query)
    
    return {
        "companies": companies,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@router.get("/companies/{company_name}")
async def get_company_details(company_name: str):
    """Get detailed information about a specific company"""
    
    company = db.companies.find_one(
        {"name": company_name},
        {"_id": 0}
    )
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Get signals for this company
    signals = list(db.signals.find(
        {"company_name": company_name},
        {"_id": 0, "company_id": 0}
    ).sort("detected_at", -1))
    
    return {
        "company": company,
        "signals": signals,
        "signal_count": len(signals)
    }