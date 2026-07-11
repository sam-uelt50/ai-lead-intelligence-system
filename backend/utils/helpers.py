# backend/utils/helpers.py
from datetime import datetime
from typing import Any, Dict

def format_datetime(dt: datetime) -> str:
    """Format datetime to ISO string"""
    return dt.isoformat() if dt else None

def clean_company_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Clean and validate company data"""
    cleaned = {}
    
    # Basic fields
    if "name" in data:
        cleaned["name"] = str(data["name"]).strip()
    
    if "website" in data and data["website"]:
        website = str(data["website"]).strip()
        if not website.startswith(("http://", "https://")):
            website = f"https://{website}"
        cleaned["website"] = website
    
    if "industry" in data and data["industry"]:
        cleaned["industry"] = str(data["industry"]).strip()
    
    if "size" in data and data["size"]:
        cleaned["size"] = str(data["size"]).strip()
    
    return cleaned

def calculate_days_ago(date_str: str) -> int:
    """Calculate days ago from ISO date string"""
    try:
        date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        delta = datetime.now() - date
        return delta.days
    except:
        return 999
