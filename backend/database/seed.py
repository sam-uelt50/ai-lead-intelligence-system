# backend/database/seed.py
import asyncio
from .mongodb import db
from datetime import datetime, timedelta

async def seed_sample_data():
    """Seed sample data into database"""
    await db.connect()
    
    # Sample data
    companies = [
        {
            "name": "CloudNine Solutions",
            "website": "https://cloudnine.example.com",
            "industry": "Cloud Computing",
            "size": "201-500 employees",
            "score": 75,
            "priority": "warm",
            "growth_signals": [
                {
                    "type": "expansion",
                    "description": "Expanding to APAC region",
                    "confidence": 80,
                    "source": "Company Blog",
                    "detected_at": datetime.now() - timedelta(days=20)
                }
            ],
            "created_at": datetime.now() - timedelta(days=180),
            "updated_at": datetime.now()
        }
    ]
    
    # Insert if not exists
    for company in companies:
        existing = await db.db.companies.find_one({"name": company["name"]})
        if not existing:
            await db.db.companies.insert_one(company)
    
    print("✅ Database seeded with sample data")
    await db.disconnect()

if __name__ == "__main__":
    asyncio.run(seed_sample_data())