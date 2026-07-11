from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from models.lead_model import LeadCreate
import motor.motor_asyncio
import os
from bson import ObjectId

# MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://samueltesema56_db_user:sam123@cluster0.4dfoa3f.mongodb.net/agency_intel?retryWrites=true&w=majority")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
db = client.agency_intel
leads_collection = db.leads

async def save_leads(leads: List[LeadCreate]):
    """Save multiple leads to database"""
    if not leads:
        print("⚠️ No leads provided to save")
        return []
    
    lead_dicts = []
    now = datetime.now()
    
    for i, lead in enumerate(leads):
        try:
            lead_dict = lead.dict()
            lead_dict.update({
                "_id": str(ObjectId()),  # Generate unique ID
                "created_at": now,
                "updated_at": now,
                "scraped_at": now,  # When it was scraped
                "imported_at": now   # When it was imported to DB
            })
            lead_dicts.append(lead_dict)
            
            # Log first 3
            if i < 3:
                print(f"   💾 Preparing: {lead.name}")
                
        except Exception as e:
            print(f"⚠️ Error preparing lead {i}: {e}")
            continue
    
    if lead_dicts:
        try:
            result = await leads_collection.insert_many(lead_dicts)
            print(f"📁 Inserted into collection: leads")
            print(f"📊 Database count after insert: {await leads_collection.count_documents({})}")
            return [str(id) for id in result.inserted_ids]
        except Exception as e:
            print(f"❌ Database insert error: {e}")
            return []
    
    return []

async def get_leads_count() -> int:
    """Get total number of leads in database"""
    try:
        return await leads_collection.count_documents({})
    except Exception as e:
        print(f"Error counting leads: {e}")
        return 0