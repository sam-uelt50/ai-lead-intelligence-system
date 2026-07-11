from backend.config import db
from backend.models.company import Company

def filter_companies_by_signals(signals):
    query = {"growth_signals": {"$in": signals}}
    results = db.companies.find(query)
    return [Company(**company) for company in results]
