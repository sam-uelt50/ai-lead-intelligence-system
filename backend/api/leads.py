# backend/api/leads.py
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from database.mongodb import db
from database.models.lead import LeadResponse
from services.scoring_service import ScoringService

router = APIRouter(prefix="/leads", tags=["leads"])

scoring_service = ScoringService()

@router.get("/", response_model=List[LeadResponse])
async def get_leads(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    status: Optional[str] = Query(None, description="Filter by lead status"),
    priority: Optional[str] = Query(None, description="Filter by priority")
):
    """Get leads with optional filtering"""
    try:
        # First get companies with high scores
        company_filters = {}
        if priority:
            company_filters["priority"] = priority
        
        companies = await db.get_companies(
            skip=skip,
            limit=limit,
            filters=company_filters,
            sort_by="score",
            sort_order=-1
        )
        
        # Convert companies to lead responses
        leads = []
        for company in companies:
            if company["score"] >= 60:  # Only include qualified leads
                leads.append({
                    "company": company,
                    "score": company["score"],
                    "priority": company["priority"],
                    "reason": _generate_lead_reason(company),
                    "next_best_action": _determine_next_action(company),
                    "estimated_conversion_probability": _estimate_conversion_probability(company)
                })
        
        # Filter by status if specified
        if status:
            leads = [lead for lead in leads if lead.get("status") == status]
        
        return leads
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/priority", response_model=List[LeadResponse])
async def get_priority_leads(
    limit: int = Query(20, ge=1, le=100)
):
    """Get highest priority leads (hot/warm)"""
    try:
        # Get hot and warm companies
        companies = await db.get_companies(
            skip=0,
            limit=limit * 2,  # Get more to filter
            filters={"priority": {"$in": ["hot", "warm"]}},
            sort_by="score",
            sort_order=-1
        )
        
        # Convert to lead responses
        leads = []
        for company in companies:
            leads.append({
                "company": company,
                "score": company["score"],
                "priority": company["priority"],
                "reason": _generate_lead_reason(company),
                "next_best_action": _determine_next_action(company),
                "estimated_conversion_probability": _estimate_conversion_probability(company),
                "signals_count": len(company.get("growth_signals", []))
            })
        
        # Sort by score and return top N
        leads.sort(key=lambda x: x["score"], reverse=True)
        return leads[:limit]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/fresh", response_model=List[LeadResponse])
async def get_fresh_leads(
    days: int = Query(7, ge=1, le=30, description="Maximum days since detection"),
    limit: int = Query(10, ge=1, le=50)
):
    """Get recently detected companies with signals"""
    # Note: This would require storing detection date on signals
    # For now, we'll return high-priority leads
    return await get_priority_leads(limit=limit)

@router.get("/stats")
async def get_lead_stats():
    """Get lead statistics"""
    try:
        stats = await db.get_stats()
        
        # Calculate lead-specific stats
        total_companies = stats.get("total_companies", 0)
        priority_counts = stats.get("priority_counts", {})
        
        qualified_leads = sum(
            count for priority, count in priority_counts.items() 
            if priority in ["hot", "warm"]
        )
        
        return {
            "total_companies": total_companies,
            "qualified_leads": qualified_leads,
            "qualification_rate": round((qualified_leads / total_companies * 100), 2) if total_companies > 0 else 0,
            "priority_distribution": priority_counts,
            "average_score": stats.get("average_score", 0),
            "signal_distribution": stats.get("signal_counts", {})
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Helper functions
def _generate_lead_reason(company: dict) -> str:
    """Generate a reason why this is a good lead"""
    signals = company.get("growth_signals", [])
    signal_types = {s.get("type") for s in signals}
    
    reasons = []
    
    if "hiring" in signal_types:
        reasons.append("Hiring marketing roles")
    
    if "funding" in signal_types:
        reasons.append("Recent funding")
    
    if "tech_refresh" in signal_types:
        reasons.append("Technology modernization")
    
    if company.get("score", 0) >= 80:
        reasons.append("High intent score")
    
    if not reasons:
        reasons.append("Strong company fit")
    
    return "; ".join(reasons)

def _determine_next_action(company: dict) -> str:
    """Determine the next best action for this lead"""
    priority = company.get("priority")
    score = company.get("score", 0)
    
    if priority == "hot":
        return "Immediate outreach - schedule intro call this week"
    elif priority == "warm":
        return "Add to outreach queue - contact within 2 weeks"
    elif score >= 50:
        return "Monitor for additional signals"
    else:
        return "Re-evaluate in 30 days"

def _estimate_conversion_probability(company: dict) -> int:
    """Estimate conversion probability based on score and signals"""
    base_probability = company.get("score", 0)
    
    # Adjust based on signal count
    signal_count = len(company.get("growth_signals", []))
    if signal_count >= 3:
        base_probability += 10
    elif signal_count >= 2:
        base_probability += 5
    
    # Adjust based on priority
    priority = company.get("priority")
    if priority == "hot":
        base_probability += 15
    elif priority == "warm":
        base_probability += 5
    
    return min(95, base_probability)  # Cap at 95%