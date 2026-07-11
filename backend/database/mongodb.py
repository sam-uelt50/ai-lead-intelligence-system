# backend/database/mongodb.py
import os
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime
from typing import List, Optional, Dict, Any
import json

from config import config

class MongoDB:
    """MongoDB database connection and operations"""
    
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
        return cls._instance
    
    async def connect(self):
        """Connect to MongoDB database"""
        if self._client is None:
            try:
                self._client = AsyncIOMotorClient(config.MONGODB_URI)
                self._db = self._client[config.DATABASE_NAME]
                print(f"✅ Connected to MongoDB: {config.DATABASE_NAME}")
                
                # Create indexes
                await self._create_indexes()
                
            except Exception as e:
                print(f"❌ MongoDB connection failed: {e}")
                raise
    
    async def _create_indexes(self):
        """Create database indexes for better performance"""
        indexes = {
            "companies": [
                [("score", -1)],  # Sort by score descending
                [("priority", 1)],  # Filter by priority
                [("industry", 1)],  # Filter by industry
                [("created_at", -1)],  # Sort by creation date
                [("growth_signals.type", 1)]  # Filter by signal type
            ],
            "leads": [
                [("company_id", 1)],
                [("status", 1)],
                [("priority", -1)]
            ]
        }
        
        for collection_name, collection_indexes in indexes.items():
            for index_fields in collection_indexes:
                try:
                    await self._db[collection_name].create_index(index_fields)
                except Exception as e:
                    print(f"Warning: Could not create index for {collection_name}: {e}")
        
        print("✅ Database indexes created")
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            print("🔌 Disconnected from MongoDB")
    
    # Company Operations
    async def insert_company(self, company_data: Dict[str, Any]) -> str:
        """Insert a new company"""
        company_data["created_at"] = datetime.now()
        company_data["updated_at"] = datetime.now()
        
        result = await self._db.companies.insert_one(company_data)
        return str(result.inserted_id)
    
    async def get_company(self, company_id: str) -> Optional[Dict[str, Any]]:
        """Get a company by ID"""
        try:
            company = await self._db.companies.find_one({"_id": ObjectId(company_id)})
            if company:
                company["_id"] = str(company["_id"])
            return company
        except:
            return None
    
    async def get_companies(
        self, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        sort_by: str = "score",
        sort_order: int = -1
    ) -> List[Dict[str, Any]]:
        """Get companies with filters"""
        query = filters or {}
        
        cursor = self._db.companies.find(query)
        
        # Apply sorting
        if sort_by:
            cursor = cursor.sort(sort_by, sort_order)
        
        # Apply pagination
        cursor = cursor.skip(skip).limit(limit)
        
        companies = []
        async for company in cursor:
            company["_id"] = str(company["_id"])
            companies.append(company)
        
        return companies
    
    async def update_company(self, company_id: str, update_data: Dict[str, Any]) -> bool:
        """Update a company"""
        update_data["updated_at"] = datetime.now()
        
        result = await self._db.companies.update_one(
            {"_id": ObjectId(company_id)},
            {"$set": update_data}
        )
        
        return result.modified_count > 0
    
    async def delete_company(self, company_id: str) -> bool:
        """Delete a company"""
        result = await self._db.companies.delete_one({"_id": ObjectId(company_id)})
        return result.deleted_count > 0
    
    async def add_signal_to_company(self, company_id: str, signal_data: Dict[str, Any]) -> bool:
        """Add a growth signal to a company"""
        signal_data["detected_at"] = datetime.now()
        
        result = await self._db.companies.update_one(
            {"_id": ObjectId(company_id)},
            {
                "$push": {"growth_signals": signal_data},
                "$set": {"updated_at": datetime.now()}
            }
        )
        
        return result.modified_count > 0
    
    # Lead Operations
    async def create_lead(self, company_id: str, lead_data: Dict[str, Any]) -> str:
        """Create a new lead from a company"""
        lead_data["company_id"] = company_id
        lead_data["created_at"] = datetime.now()
        lead_data["updated_at"] = datetime.now()
        lead_data["status"] = "new"
        
        result = await self._db.leads.insert_one(lead_data)
        return str(result.inserted_id)
    
    async def get_leads(
        self,
        skip: int = 0,
        limit: int = 50,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get leads with optional status filter"""
        query = {}
        if status:
            query["status"] = status
        
        cursor = self._db.leads.find(query).sort("priority", -1).skip(skip).limit(limit)
        
        leads = []
        async for lead in cursor:
            lead["_id"] = str(lead["_id"])
            leads.append(lead)
        
        return leads
    
    # Analytics
    async def get_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        stats = {}
        
        # Company counts by priority
        pipeline = [
            {"$group": {"_id": "$priority", "count": {"$sum": 1}}}
        ]
        
        priority_counts = {}
        async for doc in self._db.companies.aggregate(pipeline):
            priority_counts[doc["_id"]] = doc["count"]
        
        stats["priority_counts"] = priority_counts
        
        # Average score
        pipeline = [
            {"$group": {"_id": None, "avg_score": {"$avg": "$score"}}}
        ]
        
        async for doc in self._db.companies.aggregate(pipeline):
            stats["average_score"] = round(doc["avg_score"], 2)
        
        # Signal counts
        pipeline = [
            {"$unwind": "$growth_signals"},
            {"$group": {"_id": "$growth_signals.type", "count": {"$sum": 1}}}
        ]
        
        signal_counts = {}
        async for doc in self._db.companies.aggregate(pipeline):
            signal_counts[doc["_id"]] = doc["count"]
        
        stats["signal_counts"] = signal_counts
        
        # Lead counts by status
        pipeline = [
            {"$group": {"_id": "$status", "count": {"$sum": 1}}}
        ]
        
        lead_status_counts = {}
        async for doc in self._db.leads.aggregate(pipeline):
            lead_status_counts[doc["_id"]] = doc["count"]
        
        stats["lead_status_counts"] = lead_status_counts
        
        # Total counts
        stats["total_companies"] = await self._db.companies.count_documents({})
        stats["total_leads"] = await self._db.leads.count_documents({})
        
        return stats

# Database instance
db = MongoDB()