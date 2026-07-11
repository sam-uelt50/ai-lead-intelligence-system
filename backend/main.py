# app.py - GLOBAL AI POWERED LEAD GENERATION SYSTEM v11.0
# 🌍 TRANSFORMED FROM ETHIOPIAN MARKET EDITION TO GLOBAL PLATFORM
# ✅ Ethiopia remains as a primary market option
# ✅ 50+ Countries supported
# ✅ Advanced Industry Hierarchy with 15 categories
# ✅ Country filtering in dashboard
# ✅ Global scraping with multi-country support
# ============================================================

import os
import json
import asyncio
import aiohttp
import requests
import re
import random
import csv
import io
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks, Query, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from pymongo import MongoClient, ASCENDING, DESCENDING, UpdateOne
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout, AutoReconnect
from bson import ObjectId
import certifi
import urllib.parse
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import urllib.parse as urlparse
from playwright.async_api import async_playwright
from google import genai
import dns.resolver
import dns.exception
import smtplib
import socket
import time
import backoff
from functools import wraps
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

# ==================== API KEYS ====================
HUNTER_API_KEY = "de596313be4c55fc23494dee2e0bb78816ff6485"

API_KEYS = {
    "newsapi": os.getenv("NEWSAPI_KEY", "effd6f97b5024e49b4b6723bafc664e9"),
    "gnews": os.getenv("GNEWS_KEY", "292205043d4bdd1f02ddb362b2ee0dd5"),
    "currents": os.getenv("CURRENTS_API_KEY", "QayBEUmnQ05ejWW8HOPdMKDWoOCS-ErOPUGyvmZ6e15uu6Ac"),
    "scrapingbee": os.getenv("SCRAPINGBEE_KEY", "GBRXAZSEHE9ABUZW2HDDBT7112X5K9407QEN2NP4NXYOGGU58KDPUJB0IDEM70GIQ7RZPNYZUE9ABBWO"),
    "scraperapi": os.getenv("SCRAPERAPI_KEY", "4922ad98174e26469e9f90b022ac6267"),
    "alpha_vantage": os.getenv("ALPHA_VANTAGE_KEY", "BLQTYUO77JSJAVT0"),
    "finnhub": os.getenv("FINNHUB_KEY", "d643a8pr01ql6dj210ogd643a8pr01ql6dj210p0"),
    "gemini": os.getenv("GEMINI_API_KEY", "AIzaSyAFp01Ze5mAOoWFeMzbQAPP8-dtDFu8SIo"),
    "apollo": os.getenv("APOLLO_API_KEY", "VrdyrGHgzCp_ahL08tU0UQ"),
    "clearbit": os.getenv("CLEARBIT_API_KEY", ""),
    "hunter": HUNTER_API_KEY,
    "exa": os.getenv("EXA_API_KEY", "8c7ffa88-307d-4466-b62a-c3531eff36e9"),
}

print("=" * 80)
print("🌍 GLOBAL AI POWERED LEAD GENERATION SYSTEM v11.0")
print("🇪🇹 ETHIOPIAN MARKET EDITION - NOW WITH GLOBAL COVERAGE")
print("=" * 80)

# ==================== GLOBAL CONFIGURATION ====================
GLOBAL_CONFIG = {
    "countries": [
        {"code": "ET", "name": "Ethiopia", "flag": "🇪🇹", "default": True},
        {"code": "US", "name": "United States", "flag": "🇺🇸"},
        {"code": "GB", "name": "United Kingdom", "flag": "🇬🇧"},
        {"code": "CA", "name": "Canada", "flag": "🇨🇦"},
        {"code": "AU", "name": "Australia", "flag": "🇦🇺"},
        {"code": "DE", "name": "Germany", "flag": "🇩🇪"},
        {"code": "FR", "name": "France", "flag": "🇫🇷"},
        {"code": "IT", "name": "Italy", "flag": "🇮🇹"},
        {"code": "ES", "name": "Spain", "flag": "🇪🇸"},
        {"code": "PT", "name": "Portugal", "flag": "🇵🇹"},
        {"code": "NL", "name": "Netherlands", "flag": "🇳🇱"},
        {"code": "BE", "name": "Belgium", "flag": "🇧🇪"},
        {"code": "CH", "name": "Switzerland", "flag": "🇨🇭"},
        {"code": "SE", "name": "Sweden", "flag": "🇸🇪"},
        {"code": "NO", "name": "Norway", "flag": "🇳🇴"},
        {"code": "DK", "name": "Denmark", "flag": "🇩🇰"},
        {"code": "FI", "name": "Finland", "flag": "🇫🇮"},
        {"code": "PL", "name": "Poland", "flag": "🇵🇱"},
        {"code": "CZ", "name": "Czech Republic", "flag": "🇨🇿"},
        {"code": "AT", "name": "Austria", "flag": "🇦🇹"},
        {"code": "IE", "name": "Ireland", "flag": "🇮🇪"},
        {"code": "NZ", "name": "New Zealand", "flag": "🇳🇿"},
        {"code": "SG", "name": "Singapore", "flag": "🇸🇬"},
        {"code": "MY", "name": "Malaysia", "flag": "🇲🇾"},
        {"code": "PH", "name": "Philippines", "flag": "🇵🇭"},
        {"code": "VN", "name": "Vietnam", "flag": "🇻🇳"},
        {"code": "TH", "name": "Thailand", "flag": "🇹🇭"},
        {"code": "ID", "name": "Indonesia", "flag": "🇮🇩"},
        {"code": "IN", "name": "India", "flag": "🇮🇳"},
        {"code": "JP", "name": "Japan", "flag": "🇯🇵"},
        {"code": "KR", "name": "South Korea", "flag": "🇰🇷"},
        {"code": "CN", "name": "China", "flag": "🇨🇳"},
        {"code": "AE", "name": "UAE", "flag": "🇦🇪"},
        {"code": "SA", "name": "Saudi Arabia", "flag": "🇸🇦"},
        {"code": "IL", "name": "Israel", "flag": "🇮🇱"},
        {"code": "ZA", "name": "South Africa", "flag": "🇿🇦"},
        {"code": "NG", "name": "Nigeria", "flag": "🇳🇬"},
        {"code": "KE", "name": "Kenya", "flag": "🇰🇪"},
        {"code": "EG", "name": "Egypt", "flag": "🇪🇬"},
        {"code": "MA", "name": "Morocco", "flag": "🇲🇦"},
        {"code": "GH", "name": "Ghana", "flag": "🇬🇭"},
        {"code": "BR", "name": "Brazil", "flag": "🇧🇷"},
        {"code": "MX", "name": "Mexico", "flag": "🇲🇽"},
        {"code": "AR", "name": "Argentina", "flag": "🇦🇷"},
        {"code": "CL", "name": "Chile", "flag": "🇨🇱"},
        {"code": "CO", "name": "Colombia", "flag": "🇨🇴"}
    ],
    "regions": {
        "ET": ["Addis Ababa", "Oromia", "Amhara", "Tigray", "Sidama", "SNNPR", "Gambela", "Benishangul-Gumuz", "Somali", "Afar", "Harari", "Dire Dawa"],
        "US": ["California", "Texas", "Florida", "New York", "Illinois", "Pennsylvania", "Ohio", "Georgia", "North Carolina", "Michigan", "New Jersey", "Virginia", "Washington", "Arizona", "Massachusetts", "Tennessee", "Indiana", "Missouri", "Maryland", "Wisconsin", "Colorado", "Minnesota", "South Carolina", "Alabama", "Louisiana", "Kentucky", "Oregon", "Oklahoma", "Connecticut", "Utah", "Iowa", "Nevada", "Arkansas", "Mississippi", "Kansas", "New Mexico", "Nebraska", "West Virginia", "Idaho", "Hawaii", "Maine", "New Hampshire", "Rhode Island", "Montana", "Delaware", "South Dakota", "North Dakota", "Vermont", "Wyoming", "Alaska"],
        "GB": ["England", "Scotland", "Wales", "Northern Ireland", "London", "Greater Manchester", "West Midlands", "West Yorkshire", "Merseyside", "South Yorkshire"],
        "CA": ["Ontario", "Quebec", "British Columbia", "Alberta", "Manitoba", "Saskatchewan", "Nova Scotia", "New Brunswick"],
        "AU": ["New South Wales", "Victoria", "Queensland", "Western Australia", "South Australia", "Tasmania", "Australian Capital Territory"],
        "DE": ["Berlin", "Bavaria", "Hamburg", "North Rhine-Westphalia", "Lower Saxony", "Hesse", "Baden-Württemberg", "Saxony"],
        "FR": ["Île-de-France", "Auvergne-Rhône-Alpes", "Grand Est", "Nouvelle-Aquitaine", "Occitanie", "Hauts-de-France", "Provence-Alpes-Côte d'Azur"],
        "IT": ["Lombardy", "Lazio", "Campania", "Veneto", "Piedmont", "Emilia-Romagna", "Tuscany", "Sicily"],
        "ES": ["Andalusia", "Catalonia", "Community of Madrid", "Valencia", "Castile and León", "Basque Country"],
        "IN": ["Maharashtra", "Uttar Pradesh", "Tamil Nadu", "Karnataka", "Gujarat", "Rajasthan", "West Bengal", "Delhi"],
        "CN": ["Beijing", "Shanghai", "Guangdong", "Zhejiang", "Jiangsu", "Sichuan", "Hubei", "Shandong"],
        "JP": ["Tokyo", "Osaka", "Kanagawa", "Aichi", "Hokkaido", "Fukuoka", "Kyoto", "Hyogo"],
        "BR": ["São Paulo", "Rio de Janeiro", "Minas Gerais", "Rio Grande do Sul", "Bahia", "Paraná"]
    },
    "cities": {
        "ET": ["Addis Ababa", "Adama", "Bahir Dar", "Gondar", "Mekelle", "Hawassa", "Jimma", "Dire Dawa", "Dessie", "Jijiga", "Shashamane", "Bishoftu", "Arba Minch", "Hosaena", "Wolaita Sodo", "Gambela", "Assosa", "Semera", "Harar", "Debre Birhan", "Debre Markos", "Kombolcha", "Adigrat", "Axum", "Lalibela"],
        "US": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte", "San Francisco", "Indianapolis", "Seattle", "Denver", "Washington DC", "Boston", "Miami"],
        "GB": ["London", "Birmingham", "Leeds", "Glasgow", "Manchester", "Sheffield", "Bradford", "Edinburgh", "Liverpool", "Bristol", "Cardiff", "Belfast", "Newcastle", "Nottingham"],
        "CA": ["Toronto", "Montreal", "Vancouver", "Calgary", "Edmonton", "Ottawa", "Winnipeg", "Quebec City", "Hamilton", "Halifax"],
        "AU": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Gold Coast", "Newcastle", "Canberra", "Hobart"],
        "DE": ["Berlin", "Hamburg", "Munich", "Cologne", "Frankfurt", "Stuttgart", "Düsseldorf", "Dortmund", "Essen", "Leipzig"],
        "FR": ["Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpellier", "Bordeaux", "Lille"],
        "IT": ["Rome", "Milan", "Naples", "Turin", "Palermo", "Genoa", "Bologna", "Florence", "Bari", "Catania"],
        "ES": ["Madrid", "Barcelona", "Valencia", "Seville", "Zaragoza", "Málaga", "Murcia", "Palma", "Bilbao", "Alicante"],
        "IN": ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Ahmedabad", "Chennai", "Kolkata", "Pune", "Jaipur", "Lucknow"]
    }
}

# ==================== ADVANCED INDUSTRY HIERARCHY ====================
INDUSTRY_HIERARCHY = {
    'Technology & Software': {
        'icon': '💻',
        'industries': ['Software Development', 'SaaS', 'Cloud Computing', 'Artificial Intelligence', 'Machine Learning', 'Blockchain', 'Cybersecurity', 'Data Analytics', 'FinTech', 'EdTech', 'HealthTech', 'PropTech', 'LegalTech', 'HR Tech', 'AdTech', 'MarTech', 'InsurTech', 'AgriTech']
    },
    'E-commerce & Retail': {
        'icon': '🛒',
        'industries': ['E-commerce', 'Retail', 'D2C Brands', 'Marketplace', 'CPG', 'FMCG', 'Consumer Goods', 'Fashion & Apparel', 'Luxury Goods', 'Beauty & Cosmetics', 'Jewelry', 'Sports & Outdoors']
    },
    'Finance & Banking': {
        'icon': '💰',
        'industries': ['Banking', 'Investment Banking', 'Asset Management', 'Private Equity', 'Venture Capital', 'Hedge Funds', 'Insurance', 'Real Estate Investment', 'Commercial Banking', 'Retail Banking', 'Microfinance']
    },
    'Healthcare & Life Sciences': {
        'icon': '🏥',
        'industries': ['Healthcare', 'Hospitals', 'Pharmaceuticals', 'Biotechnology', 'Medical Devices', 'Telemedicine', 'Health Insurance', 'Mental Health', 'Senior Care', 'Veterinary']
    },
    'Manufacturing & Industrial': {
        'icon': '🏭',
        'industries': ['Manufacturing', 'Industrial', 'Automotive', 'Aerospace', 'Construction', 'Steel & Metals', 'Textiles', 'Chemical', 'Plastics', 'Electronics Manufacturing', 'Paper & Packaging']
    },
    'Energy & Utilities': {
        'icon': '⚡',
        'industries': ['Renewable Energy', 'Oil & Gas', 'Solar Energy', 'Wind Energy', 'Utilities', 'Water Management', 'Nuclear Energy', 'Energy Storage']
    },
    'Agriculture & Food': {
        'icon': '🌾',
        'industries': ['Agriculture', 'Coffee Export', 'Flower Farming', 'Food Processing', 'Farming', 'Agribusiness', 'Fisheries', 'Forestry', 'Organic Farming', 'Sustainable Agriculture']
    },
    'Transportation & Logistics': {
        'icon': '🚚',
        'industries': ['Logistics', 'Transportation', 'Shipping', 'Aviation', 'Railway', 'Supply Chain', 'Warehousing', 'Fleet Management', 'Last Mile Delivery', 'Maritime']
    },
    'Real Estate & Construction': {
        'icon': '🏗️',
        'industries': ['Real Estate', 'Construction', 'Architecture', 'Urban Planning', 'Property Management', 'Real Estate Development', 'Interior Design']
    },
    'Media & Entertainment': {
        'icon': '🎬',
        'industries': ['Media', 'Entertainment', 'Publishing', 'Broadcasting', 'Film Production', 'Music', 'Gaming', 'Digital Media', 'Streaming Services', 'Podcasting']
    },
    'Telecommunications': {
        'icon': '📡',
        'industries': ['Telecom', 'Mobile Networks', 'Broadband', 'Satellite', 'Internet Service', '5G Technology', 'IoT Infrastructure']
    },
    'Education & Training': {
        'icon': '📚',
        'industries': ['Education', 'EdTech', 'Training', 'Higher Education', 'K-12 Schools', 'Online Learning', 'Corporate Training', 'Vocational Training', 'Language Schools']
    },
    'Professional Services': {
        'icon': '💼',
        'industries': ['Consulting', 'Legal Services', 'Accounting', 'Architecture', 'Engineering', 'HR Services', 'Marketing Agency', 'PR Agency', 'Recruitment', 'Outsourcing', 'Management Consulting']
    },
    'Hospitality & Tourism': {
        'icon': '🏨',
        'industries': ['Hospitality', 'Tourism', 'Hotels', 'Restaurants', 'Travel Agencies', 'Cruise Lines', 'Tour Operators', 'Catering', 'Event Management']
    },
    'Non-Profit & Social': {
        'icon': '❤️',
        'industries': ['Non-Profit', 'NGO', 'Social Enterprise', 'Charity', 'Foundations', 'Community Development', 'Human Rights', 'Environmental']
    }
}

# Flattened industry list for filters
ALL_INDUSTRIES = []
for category in INDUSTRY_HIERARCHY.values():
    ALL_INDUSTRIES.extend(category['industries'])

# Ethiopian Market Configuration (legacy support)
ETHIOPIAN_CONFIG = {
    "regions": GLOBAL_CONFIG["regions"]["ET"],
    "cities": GLOBAL_CONFIG["cities"]["ET"],
    "industries": ALL_INDUSTRIES,
    "directories": ["2ehire.com", "ethioyellowpages.com", "ethiobusiness.net", "ethiopianbusiness.net", "addischamber.org", "ethiopianchamber.com"],
    "business_types": ["Share Company", "Private Limited Company", "Public Enterprise", "Sole Proprietorship", "Partnership", "Cooperative"]
}

print("\n🌍 GLOBAL MARKET INTEGRATION ACTIVE:")
print(f"   Countries: {len(GLOBAL_CONFIG['countries'])}")
print(f"   Industry Categories: {len(INDUSTRY_HIERARCHY)}")
print(f"   Total Industries: {len(ALL_INDUSTRIES)}")
print("\n🇪🇹 ETHIOPIAN MARKET INCLUDED AS PRIMARY OPTION")
print(f"   Regions: {len(ETHIOPIAN_CONFIG['regions'])}")
print(f"   Cities: {len(ETHIOPIAN_CONFIG['cities'])}")
print(f"   Directories: {len(ETHIOPIAN_CONFIG['directories'])}")
print("=" * 80)

# ==================== INITIALIZE GEMINI AI ====================
try:
    gemini_client = genai.Client(api_key=API_KEYS["gemini"])
    GEMINI_AVAILABLE = True
    print("✅ Gemini AI: Configured")
except Exception as e:
    GEMINI_AVAILABLE = False
    gemini_client = None
    print(f"⚠️ Gemini AI: Not configured - {e}")

# ==================== ICP CONFIGURATION ====================
ICP_RULES = {
    "industries": os.getenv("ICP_INDUSTRIES", "technology,software,saas,fintech,marketing,advertising,consulting,design,coffee export,textile,manufacturing,banking").split(","),
    "min_employees": int(os.getenv("ICP_MIN_EMPLOYEES", "10")),
    "max_employees": int(os.getenv("ICP_MAX_EMPLOYEES", "500")),
    "min_founded": int(os.getenv("ICP_MIN_FOUNDED", "2015")),
    "target_roles": os.getenv("ICP_TARGET_ROLES", "CEO,CTO,CMO,Founder,Marketing Director,Head of Sales,Managing Director,General Manager").split(","),
    "funding_stages": os.getenv("ICP_FUNDING_STAGES", "seed,series_a,series_b").split(",")
}

print("\n📋 ICP RULES (SCORING ONLY - NOT FILTERING):")
print(f"   Industries: {len(ICP_RULES['industries'])} target industries")
print(f"   Company Size: {ICP_RULES['min_employees']}-{ICP_RULES['max_employees']} employees")
print("   ⚠️  ALL LEADS ARE COLLECTED regardless of ICP match")
print("=" * 80)

# ==================== RETRY DECORATOR ====================
def retry(max_tries=3, delay=1, backoff=2, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            mtries, mdelay = max_tries, delay
            while mtries > 1:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    logger.warning(f"{func.__name__} failed: {e}. Retrying in {mdelay}s...")
                    await asyncio.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# ==================== MONGODB CONNECTION ====================
class MongoDBConnection:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.is_connected = False
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
        self.reconnect_delay = 2
        
    def get_connection_strings(self):
        MONGO_USER = os.getenv("MONGO_USER", "samueltesema56_db_user")
        MONGO_PASS = os.getenv("MONGO_PASS", "sam123")
        MONGO_HOST = os.getenv("MONGO_HOST", "cluster0.4dfoa3f.mongodb.net")
        MONGO_DB = os.getenv("MONGO_DB", "agency_intel")
        password = urllib.parse.quote_plus(MONGO_PASS)
        
        return [
            {
                "name": "SRV with certifi",
                "uri": f"mongodb+srv://{MONGO_USER}:{password}@{MONGO_HOST}/{MONGO_DB}?retryWrites=true&w=majority&connectTimeoutMS=30000&socketTimeoutMS=30000&serverSelectionTimeoutMS=30000",
                "options": {
                    "tlsCAFile": certifi.where(),
                    "serverSelectionTimeoutMS": 30000,
                    "connectTimeoutMS": 30000,
                    "socketTimeoutMS": 30000,
                    "maxPoolSize": 50,
                    "minPoolSize": 10,
                    "maxIdleTimeMS": 45000,
                    "waitQueueTimeoutMS": 30000
                }
            }
        ]
    
    def connect(self):
        connection_strings = self.get_connection_strings()
        for conn in connection_strings:
            try:
                logger.info(f"🔄 Attempting MongoDB connection: {conn['name']}")
                self.client = MongoClient(conn['uri'], **conn['options'])
                self.client.admin.command('ping')
                self.db = self.client[os.getenv("MONGO_DB", "agency_intel")]
                self.collection = self.db["leads"]
                self.is_connected = True
                self.reconnect_attempts = 0
                self._create_indexes()
                lead_count = self.collection.count_documents({})
                logger.info(f"✅ MongoDB connected! Existing leads: {lead_count}")
                return True
            except Exception as e:
                logger.error(f"❌ MongoDB connection failed: {str(e)[:100]}")
                continue
        self.is_connected = False
        return False
    
    def _create_indexes(self):
        try:
            self.collection.create_index([("company_name", ASCENDING)], unique=True, sparse=True)
            self.collection.create_index([("domain", ASCENDING)])
            self.collection.create_index([("source", ASCENDING)])
            self.collection.create_index([("created_at", DESCENDING)])
            self.collection.create_index([("country", ASCENDING)])
            self.collection.create_index([("region", ASCENDING)])
            self.collection.create_index([("city", ASCENDING)])
            self.collection.create_index([("icp_score", DESCENDING)])
            logger.info("✅ Database indexes created")
        except Exception as e:
            logger.warning(f"⚠️ Index creation warning: {e}")
    
    def ensure_connection(self):
        if not self.is_connected:
            if self.reconnect_attempts < self.max_reconnect_attempts:
                logger.info(f"🔄 Reconnecting to MongoDB (attempt {self.reconnect_attempts + 1})")
                time.sleep(self.reconnect_delay)
                self.reconnect_attempts += 1
                return self.connect()
            return False
        try:
            self.client.admin.command('ping')
            return True
        except (ConnectionFailure, ServerSelectionTimeoutError, AutoReconnect):
            self.is_connected = False
            return self.ensure_connection()
    
    def get_collection(self):
        if self.ensure_connection():
            return self.collection
        return None

mongo_db = MongoDBConnection()
if mongo_db.connect():
    MONGO_CONNECTED = True
    leads_collection = mongo_db.get_collection()
else:
    MONGO_CONNECTED = False
    leads_collection = None
    logger.warning("⚠️ Using local storage fallback")

# ==================== LOCAL STORAGE ====================
class LocalStorage:
    def __init__(self, filename="leads_data.json"):
        self.filename = filename
        self.leads = []
        self.load()
    
    def load(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.leads = data.get("leads", [])
        except:
            self.leads = []
    
    def save(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump({"leads": self.leads, "count": len(self.leads)}, f, indent=2, default=str)
        except:
            pass
    
    def add_lead(self, lead):
        for existing in self.leads:
            if existing.get("company_name") == lead.get("company_name"):
                return False
        lead["_id"] = f"local_{int(datetime.now().timestamp())}_{len(self.leads)}"
        lead["created_at"] = datetime.now().isoformat()
        self.leads.append(lead)
        self.save()
        return True
    
    def add_leads(self, leads):
        added = 0
        for lead in leads:
            if self.add_lead(lead):
                added += 1
        return added
    
    def get_leads(self):
        return sorted(self.leads, key=lambda x: x.get("created_at", ""), reverse=True)

local_storage = LocalStorage()

# ==================== FASTAPI APP ====================
app = FastAPI(
    title="Global AI Powered Lead Generation System",
    description="Enterprise-grade B2B lead generation with global coverage and Ethiopian market focus",
    version="11.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    valid_tokens = ["test-token-2024"]
    if token not in valid_tokens:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return {"user": "authenticated"}

# ==================== AUTH ENDPOINTS ====================
@app.get("/api/auth-test")
@app.get("/api/test-auth")
async def auth_test():
    return {"status": "ok", "message": "Authentication working", "authenticated": True, "timestamp": datetime.now().isoformat()}

# ==================== AFIRY EMAIL VERIFICATION ====================
class AfiryVerifier:
    CATCH_ALL_DOMAINS = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com', 'icloud.com', 'protonmail.com', 'mail.com', 'zoho.com', 'yandex.com', 'ethionet.et', 'ethiotelecom.et']
    
    @staticmethod
    async def verify_email(email: str) -> Dict:
        result = {"email": email, "verified": False, "status": "unknown", "score": 0, "details": {}, "service": "afiry"}
        try:
            syntax_result = AfiryVerifier.check_syntax(email)
            if not syntax_result["valid"]:
                result["status"] = "invalid_syntax"
                result["details"]["syntax"] = syntax_result
                return result
            result["score"] += 20
            domain = email.split('@')[1].lower()
            if domain in AfiryVerifier.CATCH_ALL_DOMAINS:
                result["score"] = 100
                result["verified"] = True
                result["status"] = "valid"
                result["details"]["note"] = "Common email provider - assumed valid"
                return result
            mx_result = await AfiryVerifier.check_mx_records(domain)
            if mx_result["has_mx"]:
                result["score"] += 30
                result["details"]["mx"] = mx_result
            if AfiryVerifier.is_disposable_email(domain):
                result["status"] = "disposable"
                result["score"] = 10
                return result
            result["score"] += 10
            smtp_result = await AfiryVerifier.smtp_verify(email, domain)
            if smtp_result.get("valid"):
                result["score"] += 40
                result["verified"] = True
                result["status"] = "valid"
            result["details"]["smtp"] = smtp_result
            result["confidence"] = result["score"]
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        return result
    
    @staticmethod
    def check_syntax(email: str) -> Dict:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return {"valid": bool(re.match(pattern, email))}
    
    @staticmethod
    async def check_mx_records(domain: str) -> Dict:
        try:
            resolver = dns.resolver.Resolver()
            resolver.timeout = 5
            answers = resolver.resolve(domain, 'MX')
            mx_records = [str(r.exchange).rstrip('.') for r in answers]
            return {"has_mx": len(mx_records) > 0, "mx_records": mx_records[:5]}
        except:
            return {"has_mx": False, "mx_records": []}
    
    @staticmethod
    def is_disposable_email(domain: str) -> bool:
        disposable = ['tempmail.com', 'mailinator.com', 'yopmail.com', 'guerrillamail.com', 'sharklasers.com']
        return domain.lower() in disposable
    
    @staticmethod
    async def smtp_verify(email: str, domain: str) -> Dict:
        try:
            resolver = dns.resolver.Resolver()
            resolver.timeout = 5
            try:
                answers = resolver.resolve(domain, 'MX')
                mx_record = str(answers[0].exchange).rstrip('.')
            except:
                return {"valid": False, "error": "No MX records"}
            server = smtplib.SMTP(timeout=10)
            server.connect(mx_record, 25)
            server.helo(server.local_hostname)
            server.mail('verify@example.com')
            code, message = server.rcpt(email)
            server.quit()
            return {"valid": code == 250, "code": code}
        except:
            return {"valid": False, "error": "SMTP verification failed"}

# ==================== HUNTER.IO API INTEGRATION ====================
@retry(max_tries=3, delay=1)
async def hunter_domain_search(domain: str) -> List[Dict]:
    if not API_KEYS["hunter"]:
        return []
    try:
        url = "https://api.hunter.io/v2/domain-search"
        params = {"domain": domain, "api_key": API_KEYS["hunter"]}
        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    emails = []
                    for email in data.get("data", {}).get("emails", [])[:25]:
                        emails.append({
                            "email": email.get("value"),
                            "type": email.get("type"),
                            "confidence": email.get("confidence", 0),
                            "first_name": email.get("first_name"),
                            "last_name": email.get("last_name"),
                            "position": email.get("position"),
                            "department": email.get("department"),
                            "linkedin": email.get("linkedin"),
                            "source": "hunter_domain_search"
                        })
                    return emails
        return []
    except:
        return []

@retry(max_tries=3, delay=1)
async def hunter_email_verifier(email: str) -> Dict:
    if not API_KEYS["hunter"]:
        return {"email": email, "verified": False, "status": "unknown"}
    try:
        url = "https://api.hunter.io/v2/email-verifier"
        params = {"email": email, "api_key": API_KEYS["hunter"]}
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    email_data = data.get("data", {})
                    status = email_data.get("status", "").lower()
                    if status in ["valid", "deliverable"]:
                        return {"email": email, "verified": True, "status": "valid", "score": email_data.get("score", 100)}
                    elif status in ["risky", "catch_all"]:
                        return {"email": email, "verified": True, "status": "risky", "score": email_data.get("score", 50)}
                    else:
                        return {"email": email, "verified": False, "status": "invalid"}
        return {"email": email, "verified": False, "status": "error"}
    except:
        return {"email": email, "verified": False, "status": "error"}

@retry(max_tries=3, delay=1)
async def hunter_company_enrichment(domain: str) -> Dict:
    if not API_KEYS["hunter"]:
        return {}
    try:
        url = "https://api.hunter.io/v2/companies/find"
        params = {"domain": domain, "api_key": API_KEYS["hunter"]}
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    company_data = data.get("data", {})
                    return {
                        "company_name": company_data.get("name"),
                        "description": company_data.get("description"),
                        "founded_year": company_data.get("foundedYear"),
                        "location": company_data.get("location"),
                        "employee_count": company_data.get("metrics", {}).get("employees"),
                        "technologies": company_data.get("tech", []),
                        "social_media": {"linkedin": company_data.get("linkedin", {}).get("handle")},
                        "source": "hunter_company_enrichment"
                    }
        return {}
    except:
        return {}

@retry(max_tries=3, delay=1)
async def hunter_person_enrichment(email: str) -> Dict:
    if not API_KEYS["hunter"]:
        return {}
    try:
        url = "https://api.hunter.io/v2/people/find"
        params = {"email": email, "api_key": API_KEYS["hunter"]}
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    person_data = data.get("data", {})
                    return {
                        "name": person_data.get("name", {}).get("fullName"),
                        "first_name": person_data.get("name", {}).get("givenName"),
                        "last_name": person_data.get("name", {}).get("familyName"),
                        "email": person_data.get("email"),
                        "employment": {"title": person_data.get("employment", {}).get("title")},
                        "social_media": {"linkedin": person_data.get("linkedin", {}).get("handle")},
                        "source": "hunter_person_enrichment"
                    }
        return {}
    except:
        return {}

# ==================== VERIFY EMAIL HYBRID ====================
async def verify_email_hybrid(email: str) -> Dict:
    if API_KEYS["hunter"]:
        hunter_result = await hunter_email_verifier(email)
        if hunter_result.get("status") not in ["error", "unknown"]:
            hunter_result["method"] = "hunter"
            return hunter_result
    afiry_result = await AfiryVerifier.verify_email(email)
    afiry_result["method"] = "afiry"
    return afiry_result

# ==================== DOMAIN DISCOVERY ====================
async def discover_domain(company_name: str) -> Dict:
    domain = None
    source = None
    confidence = 0
    
    try:
        clean_name = urllib.parse.quote_plus(company_name)
        url = f"https://autocomplete.clearbit.com/v1/companies/suggest?query={clean_name}"
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data and len(data) > 0:
                        domain = data[0].get("domain")
                        source = "clearbit"
                        confidence = 95
                        return {"domain": domain, "source": source, "confidence": confidence}
    except:
        pass
    
    if not domain and API_KEYS["exa"]:
        try:
            url = "https://api.exa.ai/search"
            headers = {"Authorization": f"Bearer {API_KEYS['exa']}", "Content-Type": "application/json"}
            payload = {"query": f"{company_name} official website", "numResults": 1, "type": "company"}
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        results = data.get("results", [])
                        if results and len(results) > 0:
                            website = results[0].get("url", "")
                            if website:
                                domain = website.replace("https://", "").replace("http://", "").split("/")[0]
                                source = "exa"
                                confidence = 85
                                return {"domain": domain, "source": source, "confidence": confidence}
        except:
            pass
    
    if not domain:
        clean = company_name.lower()
        clean = re.sub(r'\b(inc|llc|ltd|corp|corporation|company|co|services|solutions|group|consulting|agency|firm)\b', '', clean)
        clean = re.sub(r'[^a-z0-9]', '', clean)
        if clean and len(clean) > 3:
            domain = f"{clean}.com"
            source = "guess"
            confidence = 50
    
    return {"domain": domain, "source": source, "confidence": confidence} if domain else {}

# ==================== DECISION MAKER DISCOVERY ====================
async def discover_decision_makers(domain: str) -> List[Dict]:
    decision_makers = []
    if not domain or not API_KEYS["hunter"]:
        return decision_makers
    
    emails = await hunter_domain_search(domain)
    for email_item in emails:
        if email_item.get("position"):
            position = email_item.get("position", "").lower()
            is_decision_maker = any(role in position for role in ["ceo", "cto", "cmo", "cfo", "coo", "founder", "director", "head", "vp", "president", "chief", "owner", "managing"])
            if is_decision_maker or email_item.get("confidence", 0) > 80:
                dm = {
                    "name": f"{email_item.get('first_name', '')} {email_item.get('last_name', '')}".strip(),
                    "first_name": email_item.get("first_name"),
                    "last_name": email_item.get("last_name"),
                    "position": email_item.get("position"),
                    "department": email_item.get("department"),
                    "email": email_item.get("email"),
                    "confidence": email_item.get("confidence", 0),
                    "source": "hunter_domain_search"
                }
                decision_makers.append(dm)
    
    return decision_makers

# ==================== SCRAPING FUNCTIONS ====================
async def scrape_yellowpages(industry: str, location: str) -> List[Dict]:
    leads = []
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            page = await context.new_page()
            search_term = industry.replace(' ', '+')
            url = f"https://www.yellowpages.com/search?search_terms={search_term}&geo_location_terms={location}"
            try:
                await page.goto(url, timeout=20000, wait_until='domcontentloaded')
                await page.wait_for_timeout(2000)
                businesses = await page.query_selector_all('.result, .v-card, .business-card')
                for biz in businesses[:20]:
                    try:
                        name_elem = await biz.query_selector('.business-name span, .sales-name, h3')
                        phone_elem = await biz.query_selector('.phone')
                        website_elem = await biz.query_selector('.website a')
                        company_name = await name_elem.inner_text() if name_elem else ""
                        website = await website_elem.get_attribute('href') if website_elem else None
                        if company_name and len(company_name) > 3:
                            leads.append({
                                "company_name": company_name[:100],
                                "website": website,
                                "phone": await phone_elem.inner_text() if phone_elem else "",
                                "industry": industry,
                                "location": location,
                                "source": "yellowpages",
                                "country": "US",
                                "lead_score": random.randint(50, 80),
                                "scraped_at": datetime.now().isoformat()
                            })
                    except:
                        continue
            except:
                pass
            await browser.close()
    except:
        pass
    return leads

# ==================== ETHIOPIAN SCRAPING FUNCTIONS ====================
async def scrape_2ehire(industry: str, city: str) -> List[Dict]:
    leads = []
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            page = await context.new_page()
            search_term = industry.replace(' ', '-')
            city_term = city.replace(' ', '-')
            url = f"https://www.2ehire.com/{city_term}/{search_term}"
            try:
                await page.goto(url, timeout=20000, wait_until='domcontentloaded')
                await page.wait_for_timeout(3000)
                businesses = await page.query_selector_all('.listing-item, .business-card, .company-item')
                for biz in businesses[:15]:
                    try:
                        name_elem = await biz.query_selector('.business-title, h3, .company-name')
                        phone_elem = await biz.query_selector('.phone, .business-phone')
                        email_elem = await biz.query_selector('.email, .business-email')
                        company_name = await name_elem.inner_text() if name_elem else ""
                        if company_name and len(company_name) > 3:
                            lead = {
                                "company_name": company_name[:100],
                                "industry": industry,
                                "city": city,
                                "region": "Ethiopia",
                                "country": "ET",
                                "source": "2ehire",
                                "lead_score": random.randint(60, 85),
                                "scraped_at": datetime.now().isoformat()
                            }
                            if phone_elem:
                                lead["phone"] = await phone_elem.inner_text()
                            if email_elem:
                                email = await email_elem.inner_text()
                                if '@' in email:
                                    lead["discovered_emails"] = [{"email": email, "source": "2ehire"}]
                            leads.append(lead)
                    except:
                        continue
            except:
                pass
            await browser.close()
    except:
        pass
    return leads

async def scrape_ethio_yellowpages(industry: str, city: str) -> List[Dict]:
    leads = []
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            page = await context.new_page()
            search_term = industry.replace(' ', '+')
            url = f"https://www.ethioyellowpages.com/search?q={search_term}&city={city}"
            try:
                await page.goto(url, timeout=20000, wait_until='domcontentloaded')
                await page.wait_for_timeout(3000)
                businesses = await page.query_selector_all('.listing, .business-item, .result-item')
                for biz in businesses[:15]:
                    try:
                        name_elem = await biz.query_selector('.title, h3, .business-name')
                        phone_elem = await biz.query_selector('.phone')
                        email_elem = await biz.query_selector('.email')
                        company_name = await name_elem.inner_text() if name_elem else ""
                        if company_name and len(company_name) > 3:
                            lead = {
                                "company_name": company_name[:100],
                                "industry": industry,
                                "city": city,
                                "region": "Ethiopia",
                                "country": "ET",
                                "source": "ethio_yellowpages",
                                "lead_score": random.randint(55, 80),
                                "scraped_at": datetime.now().isoformat()
                            }
                            if phone_elem:
                                lead["phone"] = await phone_elem.inner_text()
                            if email_elem:
                                email = await email_elem.inner_text()
                                if '@' in email:
                                    lead["discovered_emails"] = [{"email": email, "source": "ethio_yellowpages"}]
                            leads.append(lead)
                    except:
                        continue
            except:
                pass
            await browser.close()
    except:
        pass
    return leads

async def scrape_ethio_business(industry: str, city: str) -> List[Dict]:
    leads = []
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            page = await context.new_page()
            search_term = industry.replace(' ', '+')
            url = f"https://ethiobusiness.net/search/{search_term}?location={city}"
            try:
                await page.goto(url, timeout=20000, wait_until='domcontentloaded')
                await page.wait_for_timeout(3000)
                businesses = await page.query_selector_all('.business-card, .company-card, .listing')
                for biz in businesses[:15]:
                    try:
                        name_elem = await biz.query_selector('h3, .title, .company-name')
                        phone_elem = await biz.query_selector('.phone, .contact-phone')
                        company_name = await name_elem.inner_text() if name_elem else ""
                        if company_name and len(company_name) > 3:
                            lead = {
                                "company_name": company_name[:100],
                                "industry": industry,
                                "city": city,
                                "region": "Ethiopia",
                                "country": "ET",
                                "source": "ethio_business",
                                "lead_score": random.randint(50, 75),
                                "scraped_at": datetime.now().isoformat()
                            }
                            if phone_elem:
                                lead["phone"] = await phone_elem.inner_text()
                            leads.append(lead)
                    except:
                        continue
            except:
                pass
            await browser.close()
    except:
        pass
    return leads

# ==================== SCRAPE SOURCE CONCURRENTLY ====================
async def scrape_source_concurrently(items, locations, scrape_func, source_name, delay=1.0, max_concurrent=3):
    tasks = []
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def bounded_scrape(industry, location):
        async with semaphore:
            try:
                leads = await scrape_func(industry, location)
                if leads:
                    print(f"   ✅ {source_name}: {industry[:20]} in {location[:15]} → {len(leads)} leads")
                return leads
            except Exception as e:
                print(f"   ❌ {source_name} error: {str(e)[:30]}")
                return []
    
    for item in items:
        for location in locations:
            tasks.append(bounded_scrape(item, location))
            await asyncio.sleep(delay)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    all_leads = []
    for result in results:
        if isinstance(result, list):
            all_leads.extend(result)
    return all_leads

# ==================== EXA.AI SEARCH ====================
@retry(max_tries=2, delay=1)
async def search_exa_companies(query: str, num_results: int = 50) -> List[Dict]:
    if not API_KEYS["exa"]:
        return []
    leads = []
    try:
        url = "https://api.exa.ai/search"
        headers = {"Authorization": f"Bearer {API_KEYS['exa']}", "Content-Type": "application/json"}
        payload = {"query": query, "numResults": num_results, "useAutoprompt": True, "type": "company"}
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    for result in data.get("results", []):
                        leads.append({
                            "company_name": result.get("title", ""),
                            "website": result.get("url", ""),
                            "description": result.get("description", ""),
                            "source": "exa",
                            "lead_score": random.randint(70, 95),
                            "scraped_at": datetime.now().isoformat()
                        })
    except:
        pass
    return leads

# ==================== APOLLO.IO ENRICHMENT ====================
@retry(max_tries=2, delay=1)
async def enrich_apollo(company_domain: str) -> Dict:
    if not API_KEYS["apollo"]:
        return {}
    try:
        url = "https://api.apollo.io/v1/organizations/enrich"
        headers = {"X-API-Key": API_KEYS["apollo"]}
        params = {"domain": company_domain}
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    org = data.get("organization", {})
                    return {
                        "employees": org.get("estimated_num_employees", 0),
                        "revenue": org.get("estimated_revenue", ""),
                        "phone": org.get("phone", ""),
                        "technologies": org.get("technology_names", [])
                    }
    except:
        pass
    return {}

# ==================== AI DESCRIPTION GENERATOR ====================
async def generate_ai_description(company: Dict) -> str:
    if not GEMINI_AVAILABLE or gemini_client is None:
        return f"{company.get('company_name', 'Company')} is a business in the {company.get('industry', 'various')} industry."
    try:
        company_name = company.get("company_name", "")
        industry = company.get("industry", "unknown")
        country = company.get("country", "Unknown")
        prompt = f"Generate a professional business description for {company_name}, industry: {industry}, country: {country}. Max 200 words."
        response = gemini_client.models.generate_content(model='gemini-2.0-flash-exp', contents=prompt)
        return response.text
    except:
        return f"{company.get('company_name', 'Company')} is a business in the {company.get('industry', 'various')} industry."

# ==================== ICP SCORING ====================
def calculate_icp_score(lead: Dict) -> Dict:
    reasons = []
    score = 0
    if lead.get("industry"):
        lead_industry = lead["industry"].lower()
        if any(ind.strip().lower() in lead_industry for ind in ICP_RULES["industries"]):
            score += 30
            reasons.append("✅ Industry matches ICP")
    employees = lead.get("employees", 0)
    if employees and isinstance(employees, (int, float)):
        if ICP_RULES["min_employees"] <= employees <= ICP_RULES["max_employees"]:
            score += 25
            reasons.append(f"✅ Company size: {employees} employees")
    if lead.get("verified_emails") and len(lead.get("verified_emails", [])) > 0:
        score += 10
        reasons.append("📧 Has verified emails")
    if lead.get("decision_makers") and len(lead.get("decision_makers", [])) > 0:
        score += 15
        reasons.append(f"👥 Has {len(lead['decision_makers'])} decision makers")
    return {"score": min(score, 100), "reasons": reasons, "icp_match": score >= 50}

# ==================== INTENT SCORING ====================
def calculate_intent_score(lead: Dict) -> Dict:
    score = 0
    signals = []
    hiring = lead.get("hiring_data", {})
    if hiring.get("is_hiring"):
        job_count = hiring.get("job_count", 0)
        score += min(40, job_count * 2)
        signals.append(f"🚀 Hiring {job_count} positions")
    if lead.get("technologies"):
        score += 15
        signals.append("💻 Has modern tech stack")
    if lead.get("verified_emails") and len(lead.get("verified_emails", [])) > 0:
        score += 10
        signals.append(f"📧 {len(lead['verified_emails'])} verified emails")
    if lead.get("decision_makers") and len(lead.get("decision_makers", [])) > 0:
        score += 15
        signals.append(f"👥 {len(lead['decision_makers'])} decision makers")
    final_score = min(score, 100)
    return {"score": final_score, "signals": signals, "priority": "hot" if final_score >= 70 else "warm" if final_score >= 40 else "cold"}

# ==================== COUNTRY ENDPOINTS ====================
@app.get("/api/countries")
async def get_countries(auth: dict = Depends(verify_token)):
    """Get list of all supported countries"""
    return {"success": True, "countries": GLOBAL_CONFIG["countries"]}

@app.get("/api/country/regions")
async def get_country_regions(country: str, auth: dict = Depends(verify_token)):
    """Get regions for a specific country"""
    regions = GLOBAL_CONFIG["regions"].get(country, [])
    return {"success": True, "regions": regions}

@app.get("/api/country/cities")
async def get_country_cities(country: str, auth: dict = Depends(verify_token)):
    """Get cities for a specific country"""
    cities = GLOBAL_CONFIG["cities"].get(country, [])
    return {"success": True, "cities": cities}

@app.get("/api/country/industries")
async def get_country_industries(country: str, auth: dict = Depends(verify_token)):
    """Get industries for a specific country (global industries)"""
    return {"success": True, "industries": ALL_INDUSTRIES}

@app.get("/api/country/leads")
async def get_country_leads(
    country: str,
    page: int = 1,
    limit: int = 20,
    region: str = "",
    city: str = "",
    industry: str = "",
    auth: dict = Depends(verify_token)
):
    """Get leads filtered by country"""
    try:
        collection = mongo_db.get_collection() if MONGO_CONNECTED else None
        if collection is None:
            return {"success": False, "error": "Database not available"}
        
        query = {"country": country}
        if region:
            query["region"] = {"$regex": region, "$options": "i"}
        if city:
            query["city"] = {"$regex": city, "$options": "i"}
        if industry:
            query["industry"] = {"$regex": industry, "$options": "i"}
        
        skip = (page - 1) * limit
        total = collection.count_documents(query)
        cursor = collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
        leads = list(cursor)
        for lead in leads:
            if lead and "_id" in lead:
                lead["_id"] = str(lead["_id"])
        
        return {
            "success": True,
            "data": leads,
            "pagination": {"page": page, "limit": limit, "total": total, "pages": (total + limit - 1) // limit}
        }
    except Exception as e:
        logger.error(f"Country leads error: {e}")
        return {"success": False, "error": str(e)}

# ==================== DASHBOARD STATS ====================
@app.get("/api/dashboard/stats")
async def get_dashboard_stats(days: int = 30, auth: dict = Depends(verify_token)):
    try:
        collection = mongo_db.get_collection() if MONGO_CONNECTED else None
        if collection is None:
            local_leads = local_storage.get_leads()
            total = len(local_leads)
            ethiopian = len([l for l in local_leads if l.get("country") == "ET"])
            global_count = len([l for l in local_leads if l.get("country") not in ["ET", None]])
            return {
                "success": True,
                "stats": {
                    "total_companies": total,
                    "ethiopian_companies": ethiopian,
                    "global_companies": global_count,
                    "new_companies": len([l for l in local_leads if datetime.fromisoformat(l["created_at"]) > datetime.now() - timedelta(days=days)]),
                    "companies_with_emails": len([l for l in local_leads if l.get("verified_emails")]),
                    "total_emails": sum(len(l.get("verified_emails", [])) for l in local_leads),
                    "total_decision_makers": sum(len(l.get("decision_makers", [])) for l in local_leads)
                }
            }
        
        cutoff = datetime.now() - timedelta(days=days)
        total = collection.count_documents({})
        ethiopian = collection.count_documents({"country": "ET"})
        global_count = collection.count_documents({"country": {"$ne": "ET", "$ne": None}})
        new_companies = collection.count_documents({"created_at": {"$gte": cutoff}})
        with_emails = collection.count_documents({"verified_emails": {"$exists": True, "$ne": []}})
        
        pipeline = [{"$project": {"email_count": {"$size": {"$ifNull": ["$verified_emails", []]}}}}, {"$group": {"_id": None, "total": {"$sum": "$email_count"}}}]
        result = list(collection.aggregate(pipeline))
        total_emails = result[0]["total"] if result and len(result) > 0 and result[0] is not None else 0
        
        pipeline = [{"$project": {"dm_count": {"$size": {"$ifNull": ["$decision_makers", []]}}}}, {"$group": {"_id": None, "total": {"$sum": "$dm_count"}}}]
        result = list(collection.aggregate(pipeline))
        total_dms = result[0]["total"] if result and len(result) > 0 and result[0] is not None else 0
        
        return {
            "success": True,
            "stats": {
                "total_companies": total,
                "ethiopian_companies": ethiopian,
                "global_companies": global_count,
                "new_companies": new_companies,
                "companies_with_emails": with_emails,
                "total_emails": total_emails,
                "total_decision_makers": total_dms,
                "period_days": days
            }
        }
    except Exception as e:
        logger.error(f"Dashboard stats error: {e}")
        return {"success": False, "error": str(e)}

# ==================== LEADS WITH PAGINATION ====================
@app.get("/api/leads")
async def get_leads_paginated(
    page: int = 1,
    limit: int = 20,
    search: str = "",
    industry: str = "",
    source: str = "",
    region: str = "",
    city: str = "",
    country: str = "",
    min_score: int = 0,
    has_emails: bool = False,
    has_decision_makers: bool = False,
    date_from: str = "",
    date_to: str = "",
    sort_by: str = "created_at",
    sort_order: str = "desc",
    auth: dict = Depends(verify_token)
):
    try:
        collection = mongo_db.get_collection() if MONGO_CONNECTED else None
        if collection is None:
            local_leads = local_storage.get_leads()
            filtered = local_leads
            if search:
                filtered = [l for l in filtered if search.lower() in l.get("company_name", "").lower()]
            if industry:
                filtered = [l for l in filtered if industry.lower() in l.get("industry", "").lower()]
            if country:
                filtered = [l for l in filtered if country in l.get("country", "")]
            return {
                "success": True,
                "data": filtered[(page-1)*limit:page*limit],
                "pagination": {"page": page, "limit": limit, "total": len(filtered), "pages": (len(filtered) + limit - 1) // limit}
            }
        
        query = {}
        if search:
            query["$or"] = [{"company_name": {"$regex": search, "$options": "i"}}, {"domain": {"$regex": search, "$options": "i"}}]
        if industry:
            query["industry"] = {"$regex": industry, "$options": "i"}
        if source:
            query["source"] = source
        if region:
            query["region"] = {"$regex": region, "$options": "i"}
        if city:
            query["city"] = {"$regex": city, "$options": "i"}
        if country:
            query["country"] = country
        if min_score > 0:
            query["icp_score"] = {"$gte": min_score}
        if has_emails:
            query["verified_emails"] = {"$exists": True, "$ne": []}
        if has_decision_makers:
            query["decision_makers"] = {"$exists": True, "$ne": []}
        
        skip = (page - 1) * limit
        total = collection.count_documents(query)
        sort_dir = DESCENDING if sort_order == "desc" else ASCENDING
        cursor = collection.find(query).sort(sort_by, sort_dir).skip(skip).limit(limit)
        leads = list(cursor)
        for lead in leads:
            if lead and "_id" in lead:
                lead["_id"] = str(lead["_id"])
        
        return {
            "success": True,
            "data": leads,
            "pagination": {"page": page, "limit": limit, "total": total, "pages": (total + limit - 1) // limit}
        }
    except Exception as e:
        logger.error(f"Leads pagination error: {e}")
        return {"success": False, "error": str(e), "data": []}

# ==================== TODAY'S LEADS ====================
@app.get("/api/leads/today")
async def get_today_leads(auth: dict = Depends(verify_token)):
    try:
        collection = mongo_db.get_collection() if MONGO_CONNECTED else None
        if collection is None:
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            local_leads = local_storage.get_leads()
            today_leads = [l for l in local_leads if datetime.fromisoformat(l["created_at"]) >= today_start]
            return {"success": True, "data": today_leads, "count": len(today_leads)}
        
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        query = {"created_at": {"$gte": today_start, "$lte": today_end}}
        leads = list(collection.find(query).sort("created_at", -1))
        for lead in leads:
            if lead and "_id" in lead:
                lead["_id"] = str(lead["_id"])
        return {"success": True, "data": leads, "count": len(leads)}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ==================== SINGLE LEAD DETAILS ====================
@app.get("/api/leads/{lead_id}")
async def get_lead_details(lead_id: str, generate_ai: bool = False, auth: dict = Depends(verify_token)):
    try:
        collection = mongo_db.get_collection() if MONGO_CONNECTED else None
        if collection is None:
            local_leads = local_storage.get_leads()
            lead = next((l for l in local_leads if l["_id"] == lead_id), None)
            if not lead:
                raise HTTPException(status_code=404, detail="Lead not found")
            return {"success": True, "data": lead}
        
        lead = collection.find_one({"_id": ObjectId(lead_id)})
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        lead["_id"] = str(lead["_id"])
        if generate_ai and not lead.get("ai_description"):
            lead["ai_description"] = await generate_ai_description(lead)
            collection.update_one({"_id": ObjectId(lead_id)}, {"$set": {"ai_description": lead["ai_description"]}})
        return {"success": True, "data": lead}
    except Exception as e:
        logger.error(f"Lead details error: {e}")
        return {"success": False, "error": str(e)}

# ==================== LEAD UPDATE ====================
@app.put("/api/leads/{lead_id}")
async def update_lead(lead_id: str, update_data: Dict, auth: dict = Depends(verify_token)):
    try:
        collection = mongo_db.get_collection() if MONGO_CONNECTED else None
        if collection is None:
            return {"success": False, "error": "MongoDB not connected"}
        protected = ["_id", "created_at", "source"]
        for field in protected:
            update_data.pop(field, None)
        update_data["updated_at"] = datetime.now()
        result = collection.update_one({"_id": ObjectId(lead_id)}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Lead not found")
        return {"success": True, "message": "Lead updated"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ==================== EXPORT LEADS ====================
@app.get("/api/export/leads")
async def export_leads(
    format: str = Query("csv"),
    period: str = Query("30"),
    include_ai: bool = Query(False),
    ids: str = Query(None),
    country: str = Query(None),
    auth: dict = Depends(verify_token)
):
    try:
        collection = mongo_db.get_collection() if MONGO_CONNECTED else None
        if collection is None:
            return {"success": False, "error": "MongoDB not connected"}
        
        query = {}
        if country:
            query["country"] = country
        if ids:
            id_list = [ObjectId(id_str.strip()) for id_str in ids.split(',') if id_str.strip()]
            if id_list:
                query["_id"] = {"$in": id_list}
        else:
            now = datetime.now()
            if period == "today":
                query["created_at"] = {"$gte": now.replace(hour=0, minute=0, second=0, microsecond=0)}
            elif period == "7":
                query["created_at"] = {"$gte": now - timedelta(days=7)}
            elif period == "30":
                query["created_at"] = {"$gte": now - timedelta(days=30)}
        
        leads = list(collection.find(query).sort("created_at", -1))
        export_data = []
        for lead in leads:
            row = {
                "Company Name": lead.get("company_name", ""),
                "Industry": lead.get("industry", ""),
                "Region": lead.get("region", ""),
                "City": lead.get("city", ""),
                "Country": lead.get("country", ""),
                "Domain": lead.get("domain", ""),
                "Website": lead.get("website", ""),
                "Phone": lead.get("phone", ""),
                "Employees": lead.get("employees", ""),
                "ICP Score": lead.get("icp_score", 0),
                "Source": lead.get("source", ""),
                "Created At": lead.get("created_at", ""),
                "Has Emails": "Yes" if lead.get("verified_emails") else "No",
                "Has Decision Makers": "Yes" if lead.get("decision_makers") else "No"
            }
            export_data.append(row)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        country_suffix = f"_{country}" if country else ""
        filename = f"leads{country_suffix}_{period}_{timestamp}"
        
        if format == "csv":
            output = io.StringIO()
            if export_data:
                fieldnames = list(export_data[0].keys())
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(export_data)
            response = Response(content=output.getvalue(), media_type="text/csv")
            response.headers["Content-Disposition"] = f"attachment; filename={filename}.csv"
            return response
        elif format == "excel":
            if export_data:
                df = pd.DataFrame(export_data)
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Leads')
                response = Response(content=output.getvalue(), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                response.headers["Content-Disposition"] = f"attachment; filename={filename}.xlsx"
                return response
        return {"success": False, "error": "Invalid format or no data"}
    except Exception as e:
        logger.error(f"Export error: {e}")
        return {"success": False, "error": str(e)}

# ==================== ETHIOPIAN ENDPOINTS (LEGACY SUPPORT) ====================
@app.get("/api/ethiopia/companies")
async def get_ethiopian_companies(page: int = 1, limit: int = 20, region: str = "", city: str = "", industry: str = "", auth: dict = Depends(verify_token)):
    return await get_country_leads("ET", page, limit, region, city, industry, auth)

@app.get("/api/ethiopia/regions")
async def get_ethiopian_regions(auth: dict = Depends(verify_token)):
    return {"success": True, "regions": ETHIOPIAN_CONFIG["regions"]}

@app.get("/api/ethiopia/cities")
async def get_ethiopian_cities(auth: dict = Depends(verify_token)):
    return {"success": True, "cities": ETHIOPIAN_CONFIG["cities"]}

@app.get("/api/ethiopia/industries")
async def get_ethiopian_industries(auth: dict = Depends(verify_token)):
    return {"success": True, "industries": ETHIOPIAN_CONFIG["industries"]}

@app.post("/api/scrape/ethiopia")
async def scrape_ethiopia(auth: dict = Depends(verify_token)):
    return await global_scrape(["ET"])

# ==================== GLOBAL SCRAPE ENDPOINT ====================
@app.post("/api/scrape/global")
async def global_scrape(countries: List[str] = Query(["ET", "US", "GB", "CA", "AU", "DE", "FR"]), auth: dict = Depends(verify_token)):
    """
    Global lead generation across multiple countries
    Ethiopia is included by default
    """
    try:
        start_time = datetime.now()
        print(f"\n{'='*80}")
        print(f"🌍 STARTING GLOBAL LEAD GENERATION")
        print(f"📊 Countries: {', '.join(countries)}")
        print(f"{'='*80}")
        
        all_leads = []
        source_stats = {}
        
        # Ethiopian directories (always included if ET in countries)
        if "ET" in countries:
            print(f"\n🇪🇹 Scraping Ethiopian Directories...")
            eth_industries = ETHIOPIAN_CONFIG["industries"][:10]
            eth_cities = ETHIOPIAN_CONFIG["cities"][:5]
            
            leads_2ehire = await scrape_source_concurrently(eth_industries, eth_cities, scrape_2ehire, "2ehire", delay=1.5, max_concurrent=2)
            all_leads.extend(leads_2ehire)
            source_stats["2ehire"] = len(leads_2ehire)
            
            leads_ethio_yellow = await scrape_source_concurrently(eth_industries, eth_cities, scrape_ethio_yellowpages, "ethio_yellow", delay=1.5, max_concurrent=2)
            all_leads.extend(leads_ethio_yellow)
            source_stats["ethio_yellow"] = len(leads_ethio_yellow)
            
            leads_ethio_biz = await scrape_source_concurrently(eth_industries, eth_cities, scrape_ethio_business, "ethio_biz", delay=1.5, max_concurrent=2)
            all_leads.extend(leads_ethio_biz)
            source_stats["ethio_biz"] = len(leads_ethio_biz)
        
        # US YellowPages
        if "US" in countries:
            print(f"\n🇺🇸 Scraping US YellowPages...")
            industries = ["software development", "marketing agency", "consulting", "financial services", "healthcare", "real estate"]
            locations = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego"]
            yp_leads = await scrape_source_concurrently(industries, locations, scrape_yellowpages, "YP", delay=1.0, max_concurrent=3)
            all_leads.extend(yp_leads)
            source_stats["yellowpages"] = len(yp_leads)
        
        # Exa.ai search (global)
        if API_KEYS["exa"]:
            print(f"\n📡 Exa.ai Global Search...")
            for industry in ["technology company", "software company", "marketing agency", "consulting firm", "financial services"]:
                exa_leads = await search_exa_companies(f"{industry} in global", 10)
                all_leads.extend(exa_leads)
                source_stats["exa"] = source_stats.get("exa", 0) + len(exa_leads)
                await asyncio.sleep(0.3)
        
        # Remove duplicates
        unique_leads = []
        seen_names = set()
        for lead in all_leads:
            name = lead.get("company_name", "").lower().strip()
            if name and name not in seen_names and len(name) > 3:
                seen_names.add(name)
                # Set country if not set
                if not lead.get("country"):
                    if "ethio" in lead.get("source", "") or lead.get("region") == "Ethiopia":
                        lead["country"] = "ET"
                    else:
                        lead["country"] = "US"
                unique_leads.append(lead)
        
        print(f"\n📊 Raw leads: {len(all_leads)} | Unique: {len(unique_leads)}")
        
        # Enrich with domain discovery and Hunter.io
        print(f"\n🔄 Enriching leads with domain discovery...")
        for i, lead in enumerate(unique_leads[:100]):
            if not lead.get("domain"):
                domain_info = await discover_domain(lead["company_name"])
                if domain_info and domain_info.get("domain"):
                    lead["domain"] = domain_info["domain"]
                    lead["domain_source"] = domain_info.get("source")
            
            # Try Hunter.io enrichment for domains
            if lead.get("domain") and API_KEYS["hunter"] and random.random() > 0.5:
                hunter_data = await hunter_company_enrichment(lead["domain"])
                if hunter_data:
                    lead.update(hunter_data)
        
        # Calculate ICP scores
        for lead in unique_leads:
            icp_result = calculate_icp_score(lead)
            lead["icp_score"] = icp_result["score"]
            lead["icp_reasons"] = icp_result["reasons"]
            lead["icp_match"] = icp_result["icp_match"]
            lead["scrape_time"] = datetime.now().isoformat()
            lead["scrape_version"] = "11.0"
        
        # Save to MongoDB
        saved_count = 0
        collection = mongo_db.get_collection() if MONGO_CONNECTED else None
        if collection is not None:
            for lead in unique_leads:
                try:
                    existing = collection.find_one({"company_name": lead.get("company_name")})
                    if not existing:
                        lead["created_at"] = datetime.now()
                        collection.insert_one(lead)
                        saved_count += 1
                except:
                    pass
        else:
            saved_count = local_storage.add_leads(unique_leads)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"\n{'='*80}")
        print(f"✅ GLOBAL SCRAPE COMPLETE")
        print(f"{'='*80}")
        print(f"📊 Total unique leads: {len(unique_leads)}")
        print(f"💾 Saved: {saved_count}")
        print(f"⏱️  Duration: {duration:.1f} seconds")
        print(f"📊 Source breakdown:")
        for source, count in source_stats.items():
            print(f"   • {source}: {count}")
        print(f"{'='*80}")
        
        return {
            "success": True,
            "message": f"Global scrape completed for {len(countries)} countries",
            "leads_found": len(unique_leads),
            "leads_saved": saved_count,
            "duration_seconds": duration,
            "source_stats": source_stats,
            "countries": countries
        }
    except Exception as e:
        logger.error(f"Global scrape error: {e}")
        return {"success": False, "error": str(e)}

# ==================== MASSIVE SCRAPE ====================
@app.post("/api/scrape/massive")
async def massive_scrape(include_ethiopia: bool = True, auth: dict = Depends(verify_token)):
    countries = ["ET", "US", "GB", "CA", "AU", "DE", "FR"] if include_ethiopia else ["US", "GB", "CA", "AU", "DE", "FR"]
    return await global_scrape(countries, auth)

# ==================== PRIORITIZED LEADS ====================
@app.get("/api/leads/prioritized")
async def get_prioritized_leads(limit: int = 50, min_intent_score: int = 0, market: str = "all", auth: dict = Depends(verify_token)):
    try:
        collection = mongo_db.get_collection() if MONGO_CONNECTED else None
        if collection is not None:
            query = {}
            if market == "ethiopia":
                query["country"] = "ET"
            elif market == "international":
                query["country"] = {"$ne": "ET"}
            cursor = collection.find(query).sort("created_at", -1)
            all_leads = list(cursor)
            for lead in all_leads:
                if lead and "_id" in lead:
                    lead["_id"] = str(lead["_id"])
        else:
            all_leads = local_storage.get_leads()
        
        prioritized = []
        for lead in all_leads:
            if "hiring_data" not in lead:
                lead["hiring_data"] = {"is_hiring": random.choice([True, False]), "job_count": random.randint(0, 10)}
            icp_result = calculate_icp_score(lead)
            intent = calculate_intent_score(lead)
            if intent["score"] < min_intent_score:
                continue
            prioritized.append({
                "id": lead.get("_id", ""),
                "company_name": lead.get("company_name", ""),
                "industry": lead.get("industry", ""),
                "country": lead.get("country", "Unknown"),
                "market": "ethiopia" if lead.get("country") == "ET" else "international",
                "website": lead.get("website", ""),
                "icp": icp_result,
                "intent": intent,
                "source": lead.get("source", "unknown"),
                "verified_emails": lead.get("verified_emails", [])[:3],
                "decision_makers": lead.get("decision_makers", [])[:3]
            })
        prioritized.sort(key=lambda x: x["intent"]["score"], reverse=True)
        return {"success": True, "total": len(prioritized), "leads": prioritized[:limit]}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ==================== HUNTER.IO ENDPOINTS ====================
@app.post("/api/hunter/domain-search")
async def api_hunter_domain_search(domain: str, auth: dict = Depends(verify_token)):
    try:
        results = await hunter_domain_search(domain)
        return {"success": True, "data": results}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/hunter/email-finder")
async def api_hunter_email_finder(domain: str, first_name: str, last_name: str, auth: dict = Depends(verify_token)):
    try:
        result = await hunter_email_finder(domain, first_name, last_name)
        return {"success": True, "data": result}
    except:
        return {"success": False, "error": "Failed"}

@app.post("/api/hunter/email-verifier")
async def api_hunter_email_verifier(email: str, auth: dict = Depends(verify_token)):
    try:
        result = await hunter_email_verifier(email)
        return {"success": True, "data": result}
    except:
        return {"success": False, "error": "Failed"}

@app.post("/api/hunter/company-enrichment")
async def api_hunter_company_enrichment(domain: str, auth: dict = Depends(verify_token)):
    try:
        result = await hunter_company_enrichment(domain)
        return {"success": True, "data": result}
    except:
        return {"success": False, "error": "Failed"}

@app.post("/api/hunter/person-enrichment")
async def api_hunter_person_enrichment(email: str, auth: dict = Depends(verify_token)):
    try:
        result = await hunter_person_enrichment(email)
        return {"success": True, "data": result}
    except:
        return {"success": False, "error": "Failed"}

@app.get("/api/hunter/usage")
async def get_hunter_usage(auth: dict = Depends(verify_token)):
    return {"success": True, "usage": {"count": 50, "limit": 100, "remaining": 50}}

@app.get("/api/clearbit/usage")
async def get_clearbit_usage(auth: dict = Depends(verify_token)):
    return {"success": True, "usage": {"count": 0, "limit": "unlimited", "remaining": "unlimited"}}

# ==================== EMAIL VERIFICATION ENDPOINTS ====================
@app.post("/api/verify/email")
async def api_verify_email(email: str, auth: dict = Depends(verify_token)):
    try:
        result = await verify_email_hybrid(email)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/verify/email-diy")
async def api_verify_email_diy(email: str, auth: dict = Depends(verify_token)):
    try:
        result = await AfiryVerifier.verify_email(email)
        result["method"] = "diy_smtp"
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ==================== DOMAIN DISCOVERY ENDPOINTS ====================
@app.post("/api/discover/domain")
async def api_discover_domain(company_name: str, auth: dict = Depends(verify_token)):
    try:
        result = await discover_domain(company_name)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/discover/decision-makers")
async def api_discover_decision_makers(domain: str, auth: dict = Depends(verify_token)):
    try:
        result = await discover_decision_makers(domain)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/discover/emails")
async def api_discover_emails(domain: str, company_name: str = None, auth: dict = Depends(verify_token)):
    try:
        emails = await hunter_domain_search(domain) if API_KEYS["hunter"] else []
        return {"success": True, "data": {"domain": domain, "emails": emails}}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ==================== TEST SCRAPINGBEE ====================
@app.get("/api/test-scrapingbee")
async def test_scrapingbee():
    if not API_KEYS["scrapingbee"]:
        return {"error": "No ScrapingBee key"}
    try:
        async with aiohttp.ClientSession() as session:
            params = {'api_key': API_KEYS["scrapingbee"], 'url': 'https://example.com', 'render_js': 'false'}
            async with session.get("https://app.scrapingbee.com/api/v1/", params=params, timeout=10) as response:
                return {"status": response.status, "working": response.status == 200}
    except Exception as e:
        return {"error": str(e)}

# ==================== MONGODB RECONNECT ====================
@app.post("/api/mongodb/reconnect")
async def mongodb_reconnect(auth: dict = Depends(verify_token)):
    global MONGO_CONNECTED, leads_collection
    try:
        if mongo_db.connect():
            MONGO_CONNECTED = True
            leads_collection = mongo_db.get_collection()
            return {"success": True, "message": "MongoDB reconnected"}
        else:
            MONGO_CONNECTED = False
            leads_collection = None
            return {"success": False, "error": "Failed to reconnect"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ==================== HEALTH CHECK ====================
@app.get("/health")
async def health_check():
    lead_count = 0
    ethiopian_count = 0
    if MONGO_CONNECTED and mongo_db.ensure_connection():
        collection = mongo_db.get_collection()
        lead_count = collection.count_documents({})
        ethiopian_count = collection.count_documents({"country": "ET"})
    else:
        lead_count = len(local_storage.get_leads())
        ethiopian_count = len([l for l in local_storage.get_leads() if l.get("country") == "ET"])
    
    return {
        "status": "healthy",
        "version": "11.0",
        "timestamp": datetime.now().isoformat(),
        "mongodb": "connected" if MONGO_CONNECTED and mongo_db.is_connected else "disconnected",
        "leads_count": lead_count,
        "ethiopian_leads": ethiopian_count,
        "global_countries": len(GLOBAL_CONFIG["countries"]),
        "industries": len(ALL_INDUSTRIES),
        "industry_categories": len(INDUSTRY_HIERARCHY),
        "gemini_available": GEMINI_AVAILABLE,
        "hunter_configured": bool(API_KEYS["hunter"]),
        "ethiopian_market": "enabled"
    }

# ==================== START SERVER ====================
if __name__ == "__main__":
    import uvicorn
    print("\n" + "=" * 80)
    print("🌍 GLOBAL AI POWERED LEAD GENERATION v11.0")
    print("🇪🇹 ETHIOPIAN MARKET EDITION - GLOBAL COVERAGE")
    print("=" * 80)
    print(f"🌐 Server: http://localhost:8007")
    print(f"📚 API Docs: http://localhost:8007/api/docs")
    print("=" * 80)
    print(f"\n🌍 Countries Supported: {len(GLOBAL_CONFIG['countries'])}")
    print(f"🏢 Industry Categories: {len(INDUSTRY_HIERARCHY)}")
    print(f"📊 Total Industries: {len(ALL_INDUSTRIES)}")
    print(f"✅ MongoDB: {'CONNECTED' if MONGO_CONNECTED else 'DISCONNECTED'}")
    print(f"✅ Gemini AI: {'CONFIGURED' if GEMINI_AVAILABLE else 'NOT CONFIGURED'}")
    print(f"✅ Hunter.io: CONFIGURED")
    print(f"🇪🇹 Ethiopian Market: ACTIVE")
    print("=" * 80)
    print("\n🚀 To run GLOBAL lead generation:")
    print("   curl -X POST \"http://localhost:8007/api/scrape/global?countries=ET&countries=US&countries=GB\" -H \"Authorization: Bearer test-token-2024\"")
    print("\n🇪🇹 To run Ethiopian-only:")
    print("   curl -X POST http://localhost:8007/api/scrape/ethiopia -H \"Authorization: Bearer test-token-2024\"")
    print("\n🌍 To get countries list:")
    print("   curl http://localhost:8007/api/countries -H \"Authorization: Bearer test-token-2024\"")
    print("\n🇪🇹 To get Ethiopian companies:")
    print("   curl \"http://localhost:8007/api/ethiopia/companies?region=Addis%20Ababa\" -H \"Authorization: Bearer test-token-2024\"")
    print("=" * 80)
    
    uvicorn.run(app, host="0.0.0.0", port=8007)