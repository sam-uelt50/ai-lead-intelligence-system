from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Optional
import asyncio
from datetime import datetime

# Import both scrapers
from services.scraper_service import AgencyLeadScraper as SampleScraper
from services.real_scraper import RealWebScraper
from services.data_service import save_leads
from models.lead_model import LeadCreate, LeadSource

router = APIRouter()
sample_scraper = SampleScraper()
real_scraper = RealWebScraper()

@router.post("/start", summary="Start web scraping")
async def start_scraping(
    background_tasks: BackgroundTasks,
    industry: str = "marketing",
    location: str = "",
    limit: int = 10,
    mode: str = "sample",  # "sample" or "real"
    save_to_db: bool = True
):
    """
    Start scraping leads and save to database.
    
    Parameters:
    - industry: marketing, technology, consulting, etc.
    - location: Optional city/state
    - limit: Number of leads to get
    - mode: "sample" (always works) or "real" (uses real sources)
    - save_to_db: Whether to save leads to database (REQUIRED for saving)
    """
    job_id = f"scrape_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        if mode == "real":
            # Use real scraper
            leads = await real_scraper.get_agency_leads(industry, location, limit)
            source = "real_web"
        else:
            # Use sample scraper (default)
            leads = await sample_scraper.scrape_agency_leads(industry, location, limit)
            source = "sample_data"
        
        # Save to database in background if requested
        saved_count = 0
        if save_to_db and leads:
            # Run saving in background
            background_tasks.add_task(
                save_leads_to_database,
                leads,
                industry,
                source
            )
            saved_count = len(leads)
        
        return {
            "success": True,
            "message": f"Scraping completed using {mode} mode",
            "job_id": job_id,
            "leads_found": len(leads),
            "leads_saved": saved_count,
            "source": source,
            "leads": leads[:20],  # Return first 20
            "mode_used": mode,
            "saved_to_db": save_to_db,
            "database_note": "Leads are being saved in background. Check /api/leads in 5 seconds."
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Scraping failed: {str(e)}"
        )

@router.post("/quick", summary="Quick scrape for dashboard")
async def quick_scrape(
    background_tasks: BackgroundTasks
):
    """Quick scrape - automatically saves to database"""
    try:
        leads = await sample_scraper.scrape_agency_leads(
            industry="marketing",
            location="",
            limit_per_source=5
        )
        
        # Save to database in background
        saved_count = 0
        if leads:
            background_tasks.add_task(
                save_leads_to_database,
                leads,
                "marketing",
                "quick_scrape"
            )
            saved_count = len(leads)
        
        return {
            "success": True,
            "message": "Quick scrape completed",
            "leads_found": len(leads),
            "leads_saved": saved_count,
            "sample_leads": leads[:3],
            "database_note": "Leads are being saved to MongoDB in background."
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Quick scrape failed: {str(e)}"
        )

@router.post("/real", summary="Real web scraping")
async def real_scrape(
    background_tasks: BackgroundTasks,
    industry: str = "marketing",
    location: str = "",
    limit: int = 10
):
    """Real web scraping using public sources - auto-saves to database"""
    try:
        leads = await real_scraper.get_agency_leads(industry, location, limit)
        
        # Save to database in background
        saved_count = 0
        if leads:
            background_tasks.add_task(
                save_leads_to_database,
                leads,
                industry,
                "real_web_sources"
            )
            saved_count = len(leads)
        
        return {
            "success": True,
            "message": "Real web scraping completed",
            "leads_found": len(leads),
            "leads_saved": saved_count,
            "source": "real_web_sources",
            "leads": leads[:20],
            "database_note": "Leads are being saved to MongoDB in background."
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Real scraping failed: {str(e)}"
        )

@router.get("/test", summary="Test scraping")
async def test_scrape(
    mode: str = "sample",
    industry: str = "marketing"
):
    """Test the scraper (doesn't save to database)"""
    try:
        if mode == "real":
            leads = await real_scraper.get_agency_leads(industry, "", 3)
        else:
            leads = await sample_scraper.scrape_agency_leads(industry, "", 3)
        
        return {
            "success": True,
            "mode": mode,
            "leads_found": len(leads),
            "leads": leads[:3],  # Return only 3 for testing
            "note": "Test mode - leads NOT saved to database. Use /start with save_to_db=true to save."
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Test failed: {str(e)}"
        )

@router.get("/status/{job_id}", summary="Check scraping job status")
async def get_scraping_status(job_id: str):
    """Get status of a scraping job"""
    # In a real app, you'd store job status in database
    return {
        "job_id": job_id,
        "status": "completed",
        "message": "Job completed successfully",
        "check_database": "Visit /api/leads to see saved leads"
    }

@router.get("/sources", summary="Available scraping sources")
async def get_sources():
    """Get available scraping sources"""
    return {
        "sources": [
            {
                "name": "sample_data",
                "description": "High-quality sample data (always works)",
                "endpoint": "/api/scrape/start?mode=sample&save_to_db=true",
                "method": "POST",
                "saves_to_db": "Yes, when save_to_db=true"
            },
            {
                "name": "real_web",
                "description": "Real web scraping (public APIs & allowed sites)",
                "endpoint": "/api/scrape/start?mode=real&save_to_db=true",
                "method": "POST",
                "saves_to_db": "Yes, when save_to_db=true"
            }
        ],
        "quick_endpoints": [
            {
                "name": "quick_scrape",
                "description": "Quick marketing agency scrape - AUTO-SAVES to database",
                "endpoint": "/api/scrape/quick",
                "method": "POST",
                "saves_to_db": "YES, automatically"
            },
            {
                "name": "real_scrape",
                "description": "Real web scraping - AUTO-SAVES to database",
                "endpoint": "/api/scrape/real",
                "method": "POST",
                "saves_to_db": "YES, automatically"
            },
            {
                "name": "test_scrape",
                "description": "Test scraping without saving",
                "endpoint": "/api/scrape/test",
                "method": "GET",
                "saves_to_db": "NO, test only"
            }
        ]
    }

# ============================================================================
# DATABASE SAVING FUNCTIONS
# ============================================================================

async def save_leads_to_database(leads: List[Dict], industry: str, source: str):
    """Background task to save leads to MongoDB"""
    try:
        print(f"\n💾 DATABASE SAVE STARTED")
        print(f"   Leads to save: {len(leads)}")
        print(f"   Industry: {industry}")
        print(f"   Source: {source}")
        
        if not leads:
            print("⚠️ No leads to save")
            return []
        
        lead_models = []
        for i, lead in enumerate(leads):
            try:
                # Get primary contact email
                primary_email = ""
                if lead.get('contacts') and len(lead['contacts']) > 0:
                    primary_email = lead['contacts'][0].get('email', '')
                
                # Create LeadCreate model
                lead_model = LeadCreate(
                    name=lead.get('company_name', lead.get('name', f'Company {i+1}')),
                    company=lead.get('company_name', lead.get('name', '')),
                    email=primary_email or lead.get('email', f'contact@example{i+1}.com'),
                    phone=lead.get('phone', f'({i+1:03}) 555-1234'),
                    website=lead.get('website', f'https://example{i+1}.com'),
                    address=lead.get('address', lead.get('location', '123 Main St')),
                    industry=lead.get('industry', industry),
                    tags=[source, industry, lead.get('priority', 'medium')],
                    notes=f"Lead score: {lead.get('lead_score', 0)}/100. Source: {source}. {lead.get('recommended_action', '')}",
                    source=LeadSource.WEB_SCRAPE,
                    priority=lead.get('priority_level', 2),
                    status="new"
                )
                lead_models.append(lead_model)
                
                if i < 3:  # Log first 3 leads
                    print(f"   📝 Lead {i+1}: {lead_model.name}")
                
            except Exception as e:
                print(f"⚠️ Error converting lead {i+1}: {e}")
                continue
        
        # Save to database
        if lead_models:
            saved_ids = await save_leads(lead_models)
            print(f"✅ SUCCESS: Saved {len(saved_ids)} leads to MongoDB")
            print(f"   Database: agency_intel")
            print(f"   Collection: leads")
            return saved_ids
        else:
            print("⚠️ No valid leads to save")
            return []
            
    except Exception as e:
        print(f"❌ ERROR saving leads to database: {str(e)}")
        return []