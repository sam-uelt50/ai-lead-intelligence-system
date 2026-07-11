# backend/api/companies.py
from fastapi import APIRouter, HTTPException, Query, Depends, BackgroundTasks
from typing import List, Optional
from bson import ObjectId

from database.mongodb import db
from database.models.company import CompanyCreate, CompanyUpdate, CompanyResponse
from services.signal_detector import SignalDetector
from services.scoring_service import ScoringService

router = APIRouter(prefix="/companies", tags=["companies"])

scoring_service = ScoringService()

@router.get("/", response_model=List[CompanyResponse])
async def get_companies(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum records to return"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    min_score: int = Query(0, ge=0, le=100, description="Minimum score"),
    industry: Optional[str] = Query(None, description="Filter by industry"),
    sort_by: str = Query("score", description="Field to sort by"),
    sort_order: int = Query(-1, ge=-1, le=1, description="Sort order: -1 for descending, 1 for ascending")
):
    """Get companies with filtering and sorting"""
    try:
        # Build query filters
        filters = {}
        
        if priority:
            filters["priority"] = priority
        
        if min_score > 0:
            filters["score"] = {"$gte": min_score}
        
        if industry:
            filters["industry"] = {"$regex": industry, "$options": "i"}
        
        companies = await db.get_companies(
            skip=skip,
            limit=limit,
            filters=filters,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        return companies
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(company_id: str):
    """Get a specific company by ID"""
    try:
        company = await db.get_company(company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        return company
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=dict)
async def create_company(
    company: CompanyCreate,
    background_tasks: BackgroundTasks,
    detect_signals: bool = Query(True, description="Automatically detect signals")
):
    """Create a new company"""
    try:
        # Create company
        company_dict = company.dict()
        company_id = await db.insert_company(company_dict)
        
        # Trigger signal detection in background if requested
        if detect_signals:
            background_tasks.add_task(
                detect_and_score_company,
                company_id,
                company_dict
            )
            return {
                "message": "Company created. Signal detection in progress.",
                "company_id": company_id,
                "detection_status": "queued"
            }
        
        return {
            "message": "Company created",
            "company_id": company_id,
            "detection_status": "skipped"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{company_id}")
async def update_company(company_id: str, update_data: CompanyUpdate):
    """Update a company"""
    try:
        success = await db.update_company(company_id, update_data.dict(exclude_unset=True))
        if not success:
            raise HTTPException(status_code=404, detail="Company not found")
        
        return {"message": "Company updated successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{company_id}")
async def delete_company(company_id: str):
    """Delete a company"""
    try:
        success = await db.delete_company(company_id)
        if not success:
            raise HTTPException(status_code=404, detail="Company not found")
        
        return {"message": "Company deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{company_id}/detect-signals")
async def detect_signals(company_id: str):
    """Manually trigger signal detection for a company"""
    try:
        company = await db.get_company(company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        async with SignalDetector() as detector:
            signals = await detector.detect_all_signals(company)
            
            # Add signals to company
            for signal in signals: