# backend/api/research.py
from fastapi import APIRouter, HTTPException

from database.mongodb import db
from services.research_service import ResearchService

router = APIRouter(prefix="/research", tags=["research"])

research_service = ResearchService()

@router.get("/{company_id}/brief")
async def generate_research_brief(company_id: str):
    """Generate a research brief for a company"""
    try:
        company = await db.get_company(company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        brief = research_service.generate_brief(company)
        
        # Update company with brief
        await db.update_company(company_id, {"research_brief": brief})
        
        return {
            "company_id": company_id,
            "company_name": company["name"],
            "brief": brief
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))