# backend/settings.py - GLOBAL AI POWERED LEAD GENERATION SYSTEM
"""
Complete configuration for Global AI Powered Lead Generation System
Supports:
- 50+ Countries
- Advanced Industry Hierarchy (15 categories, 150+ industries)
- Ethiopian Market Integration
- Multiple API Integrations
- MongoDB Atlas with failover
- Redis caching (optional)
- Rate limiting
- Environment-based configuration
"""

import os
import json
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timedelta
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load environment variables
load_dotenv()

# ==================== GLOBAL CONSTANTS ====================
# These are loaded here for compatibility with the rest of the system

GLOBAL_COUNTRIES = [
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
]

# Ethiopian Configuration (legacy support)
ETHIOPIAN_CONFIG = {
    "regions": [
        "Addis Ababa", "Oromia", "Amhara", "Tigray", "Sidama",
        "SNNPR", "Gambela", "Benishangul-Gumuz", "Somali",
        "Afar", "Harari", "Dire Dawa"
    ],
    "cities": [
        "Addis Ababa", "Adama", "Bahir Dar", "Gondar", "Mekelle",
        "Hawassa", "Jimma", "Dire Dawa", "Dessie", "Jijiga",
        "Shashamane", "Bishoftu", "Arba Minch", "Hosaena",
        "Wolaita Sodo", "Gambela", "Assosa", "Semera", "Harar",
        "Debre Birhan", "Debre Markos", "Kombolcha", "Adigrat",
        "Axum", "Lalibela"
    ],
    "industries": [
        "Coffee Export", "Textile & Garment", "Leather Products",
        "Flower Farming", "Agriculture", "Construction",
        "Banking & Finance", "Insurance", "Telecom",
        "Manufacturing", "Mining", "Tourism & Hospitality",
        "Transport & Logistics", "Education", "Healthcare",
        "Real Estate", "Retail", "Import/Export",
        "Technology", "Media & Entertainment", "Food Processing",
        "Pharmaceuticals", "Chemical Industry", "Metal & Engineering",
        "Plastic & Rubber"
    ],
    "directories": [
        "2ehire.com",
        "ethioyellowpages.com",
        "ethiobusiness.net",
        "ethiopianbusiness.net",
        "addischamber.org",
        "ethiopianchamber.com"
    ]
}

# Advanced Industry Hierarchy
INDUSTRY_HIERARCHY = {
    'Technology & Software': {
        'icon': '💻',
        'industries': [
            'Software Development', 'SaaS', 'Cloud Computing', 'Artificial Intelligence',
            'Machine Learning', 'Blockchain', 'Cybersecurity', 'Data Analytics',
            'FinTech', 'EdTech', 'HealthTech', 'PropTech', 'LegalTech',
            'HR Tech', 'AdTech', 'MarTech', 'InsurTech', 'AgriTech'
        ]
    },
    'E-commerce & Retail': {
        'icon': '🛒',
        'industries': [
            'E-commerce', 'Retail', 'D2C Brands', 'Marketplace',
            'CPG', 'FMCG', 'Consumer Goods', 'Fashion & Apparel',
            'Luxury Goods', 'Beauty & Cosmetics', 'Jewelry', 'Sports & Outdoors'
        ]
    },
    'Finance & Banking': {
        'icon': '💰',
        'industries': [
            'Banking', 'Investment Banking', 'Asset Management', 'Private Equity',
            'Venture Capital', 'Hedge Funds', 'Insurance', 'Real Estate Investment',
            'Commercial Banking', 'Retail Banking', 'Microfinance'
        ]
    },
    'Healthcare & Life Sciences': {
        'icon': '🏥',
        'industries': [
            'Healthcare', 'Hospitals', 'Pharmaceuticals', 'Biotechnology',
            'Medical Devices', 'Telemedicine', 'Health Insurance',
            'Mental Health', 'Senior Care', 'Veterinary'
        ]
    },
    'Manufacturing & Industrial': {
        'icon': '🏭',
        'industries': [
            'Manufacturing', 'Industrial', 'Automotive', 'Aerospace',
            'Construction', 'Steel & Metals', 'Textiles', 'Chemical',
            'Plastics', 'Electronics Manufacturing', 'Paper & Packaging'
        ]
    },
    'Energy & Utilities': {
        'icon': '⚡',
        'industries': [
            'Renewable Energy', 'Oil & Gas', 'Solar Energy', 'Wind Energy',
            'Utilities', 'Water Management', 'Nuclear Energy', 'Energy Storage'
        ]
    },
    'Agriculture & Food': {
        'icon': '🌾',
        'industries': [
            'Agriculture', 'Coffee Export', 'Flower Farming', 'Food Processing',
            'Farming', 'Agribusiness', 'Fisheries', 'Forestry',
            'Organic Farming', 'Sustainable Agriculture'
        ]
    },
    'Transportation & Logistics': {
        'icon': '🚚',
        'industries': [
            'Logistics', 'Transportation', 'Shipping', 'Aviation',
            'Railway', 'Supply Chain', 'Warehousing', 'Fleet Management',
            'Last Mile Delivery', 'Maritime'
        ]
    },
    'Real Estate & Construction': {
        'icon': '🏗️',
        'industries': [
            'Real Estate', 'Construction', 'Architecture', 'Urban Planning',
            'Property Management', 'Real Estate Development', 'Interior Design'
        ]
    },
    'Media & Entertainment': {
        'icon': '🎬',
        'industries': [
            'Media', 'Entertainment', 'Publishing', 'Broadcasting',
            'Film Production', 'Music', 'Gaming', 'Digital Media',
            'Streaming Services', 'Podcasting'
        ]
    },
    'Telecommunications': {
        'icon': '📡',
        'industries': [
            'Telecom', 'Mobile Networks', 'Broadband', 'Satellite',
            'Internet Service', '5G Technology', 'IoT Infrastructure'
        ]
    },
    'Education & Training': {
        'icon': '📚',
        'industries': [
            'Education', 'EdTech', 'Training', 'Higher Education',
            'K-12 Schools', 'Online Learning', 'Corporate Training',
            'Vocational Training', 'Language Schools'
        ]
    },
    'Professional Services': {
        'icon': '💼',
        'industries': [
            'Consulting', 'Legal Services', 'Accounting', 'Architecture',
            'Engineering', 'HR Services', 'Marketing Agency', 'PR Agency',
            'Recruitment', 'Outsourcing', 'Management Consulting'
        ]
    },
    'Hospitality & Tourism': {
        'icon': '🏨',
        'industries': [
            'Hospitality', 'Tourism', 'Hotels', 'Restaurants',
            'Travel Agencies', 'Cruise Lines', 'Tour Operators',
            'Catering', 'Event Management'
        ]
    },
    'Non-Profit & Social': {
        'icon': '❤️',
        'industries': [
            'Non-Profit', 'NGO', 'Social Enterprise', 'Charity',
            'Foundations', 'Community Development', 'Human Rights',
            'Environmental'
        ]
    }
}

# Flattened industry list
ALL_INDUSTRIES = []
for category in INDUSTRY_HIERARCHY.values():
    ALL_INDUSTRIES.extend(category['industries'])

# ICP Rules
ICP_RULES = {
    "industries": os.getenv("ICP_INDUSTRIES", "technology,software,saas,fintech,marketing,advertising,consulting,design,coffee export,textile,manufacturing,banking").split(","),
    "min_employees": int(os.getenv("ICP_MIN_EMPLOYEES", "10")),
    "max_employees": int(os.getenv("ICP_MAX_EMPLOYEES", "500")),
    "min_founded": int(os.getenv("ICP_MIN_FOUNDED", "2015")),
    "target_roles": os.getenv("ICP_TARGET_ROLES", "CEO,CTO,CMO,Founder,Marketing Director,Head of Sales,Managing Director,General Manager").split(","),
    "funding_stages": os.getenv("ICP_FUNDING_STAGES", "seed,series_a,series_b").split(",")
}

# Source Configuration
SOURCES = [
    {"id": "exa", "name": "Exa.ai", "icon": "🔎", "color": "badge-exa", "enabled": True},
    {"id": "yellowpages", "name": "YellowPages", "icon": "📚", "color": "badge-yellowpages", "enabled": True},
    {"id": "clearbit", "name": "Clearbit", "icon": "💡", "color": "badge-clearbit", "enabled": True},
    {"id": "apollo", "name": "Apollo.io", "icon": "🚀", "color": "badge-apollo", "enabled": True},
    {"id": "hunter", "name": "Hunter.io", "icon": "📧", "color": "badge-hunter", "enabled": True},
    {"id": "website", "name": "Website Email", "icon": "🌐", "color": "badge-website", "enabled": True},
    {"id": "2ehire", "name": "2Ehire Ethiopia", "icon": "🇪🇹", "color": "badge-ethiopia", "enabled": True},
    {"id": "ethioyellow", "name": "Ethio Yellow Pages", "icon": "📒", "color": "badge-ethiopia", "enabled": True},
    {"id": "ethiobusiness", "name": "Ethio Business", "icon": "🏢", "color": "badge-ethiopia", "enabled": True},
    {"id": "global_api", "name": "Global API", "icon": "🌍", "color": "badge-global", "enabled": True}
]


class Settings:
    """Application settings - Complete configuration for Global AI Powered Lead Generation System"""
    
    # ==================== APPLICATION ====================
    APP_NAME: str = "Global AI Powered Lead Generation System"
    APP_VERSION: str = "11.0.0"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # ==================== SERVER ====================
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8007"))
    
    # ==================== CORS ====================
    ALLOWED_ORIGINS: List[str] = os.getenv(
        "ALLOWED_ORIGINS", 
        "http://localhost:3000,http://localhost:5500,http://localhost:8007,http://127.0.0.1:8007,*"
    ).split(",")
    ALLOWED_HOSTS: List[str] = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,0.0.0.0").split(",")
    
    # ==================== MONGODB ATLAS ====================
    MONGO_USER: str = os.getenv("MONGO_USER", "samueltesema56_db_user")
    MONGO_PASS: str = os.getenv("MONGO_PASS", "sam123")
    MONGO_HOST: str = os.getenv("MONGO_HOST", "cluster0.4dfoa3f.mongodb.net")
    MONGO_DB: str = os.getenv("MONGO_DB", "agency_intel")
    MONGO_PARAMS: str = os.getenv("MONGO_PARAMS", "?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true")
    
    @property
    def MONGODB_URI(self) -> str:
        """Build MongoDB URI with credentials"""
        password = quote_plus(self.MONGO_PASS)
        return f"mongodb+srv://{self.MONGO_USER}:{password}@{self.MONGO_HOST}/{self.MONGO_DB}{self.MONGO_PARAMS}"
    
    MONGODB_URL: str = MONGODB_URI  # Alias for compatibility
    MONGODB_DB: str = MONGO_DB      # Alias for compatibility
    DATABASE_NAME: str = MONGO_DB   # For compatibility
    RANGE_DB: str = MONGO_DB        # For compatibility
    
    # ==================== DATABASE COLLECTIONS ====================
    LEADS_COLLECTION: str = "leads"
    USERS_COLLECTION: str = "users"
    SCRAPING_JOBS_COLLECTION: str = "scraping_jobs"
    COUNTRIES_COLLECTION: str = "countries"
    INDUSTRIES_COLLECTION: str = "industries"
    
    # ==================== REDIS (Optional) ====================
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    REDIS_ENABLED: bool = os.getenv("REDIS_ENABLED", "False").lower() == "true"
    
    # ==================== API KEYS ====================
    
    # ----- NEWS APIS -----
    NEWSAPI_KEY: str = os.getenv("NEWSAPI_KEY", "effd6f97b5024e49b4b6723bafc664e9")
    GNEWS_KEY: str = os.getenv("GNEWS_KEY", "292205043d4bdd1f02ddb362b2ee0dd5")
    CURRENTS_API_KEY: str = os.getenv("CURRENTS_API_KEY", "QayBEUmnQ05ejWW8HOPdMKDWoOCS-ErOPUGyvmZ6e15uu6Ac")
    
    # ----- WEB SCRAPING APIS -----
    SCRAPINGBEE_KEY: str = os.getenv("SCRAPINGBEE_KEY", "GBRXAZSEHE9ABUZW2HDDBT7112X5K9407QEN2NP4NXYOGGU58KDPUJB0IDEM70GIQ7RZPNYZUE9ABBWO")
    SCRAPERAPI_KEY: str = os.getenv("SCRAPERAPI_KEY", "4922ad98174e26469e9f90b022ac6267")
    
    # ----- FINANCIAL DATA APIS -----
    ALPHA_VANTAGE_KEY: str = os.getenv("ALPHA_VANTAGE_KEY", "BLQTYUO77JSJAVT0")
    FINNHUB_KEY: str = os.getenv("FINNHUB_KEY", "d643a8pr01ql6dj210ogd643a8pr01ql6dj210p0")
    
    # ----- AI APIS -----
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "AIzaSyAFp01Ze5mAOoWFeMzbQAPP8-dtDFu8SIo")
    
    # ----- LEAD GENERATION APIS -----
    HUNTER_API_KEY: str = os.getenv("HUNTER_API_KEY", "de596313be4c55fc23494dee2e0bb78816ff6485")
    CLEARBIT_API_KEY: str = os.getenv("CLEARBIT_API_KEY", "")
    APOLLO_API_KEY: str = os.getenv("APOLLO_API_KEY", "VrdyrGHgzCp_ahL08tU0UQ")
    EXA_API_KEY: str = os.getenv("EXA_API_KEY", "8c7ffa88-307d-4466-b62a-c3531eff36e9")
    BUILTWITH_API_KEY: str = os.getenv("BUILTWITH_API_KEY", "")
    PDL_API_KEY: str = os.getenv("PDL_API_KEY", "")
    LINKEDIN_API_KEY: str = os.getenv("LINKEDIN_API_KEY", "")
    CRUNCHBASE_API_KEY: str = os.getenv("CRUNCHBASE_API_KEY", "")
    INDEED_API_KEY: str = os.getenv("INDEED_API_KEY", "")
    
    # ==================== SECURITY ====================
    SECRET_KEY: str = os.getenv("SECRET_KEY", "test-token-2024")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # ==================== RATE LIMITING ====================
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "False").lower() == "true"
    
    # ==================== SCRAPING CONFIGURATION ====================
    MAX_SCRAPE_RESULTS: int = int(os.getenv("MAX_SCRAPE_RESULTS", "1000"))
    SCRAPE_TIMEOUT_SECONDS: int = int(os.getenv("SCRAPE_TIMEOUT_SECONDS", "300"))
    ENABLE_REAL_SCRAPING: bool = os.getenv("ENABLE_REAL_SCRAPING", "True").lower() == "true"
    CONCURRENT_SCRAPERS: int = int(os.getenv("CONCURRENT_SCRAPERS", "5"))
    RATE_LIMIT_DELAY: float = float(os.getenv("RATE_LIMIT_DELAY", "1.0"))
    
    # ==================== GLOBAL SCRAPING ====================
    GLOBAL_SCRAPING_ENABLED: bool = os.getenv("GLOBAL_SCRAPING_ENABLED", "True").lower() == "true"
    ETHIOPIAN_MARKET_ENABLED: bool = os.getenv("ETHIOPIAN_MARKET_ENABLED", "True").lower() == "true"
    DEFAULT_COUNTRIES: List[str] = os.getenv("DEFAULT_COUNTRIES", "ET,US,GB,CA,AU,DE,FR").split(",")
    
    # ==================== ENRICHMENT CONFIGURATION ====================
    ENABLE_NEWS_ENRICHMENT: bool = os.getenv("ENABLE_NEWS_ENRICHMENT", "True").lower() == "true"
    ENABLE_FINANCIAL_ENRICHMENT: bool = os.getenv("ENABLE_FINANCIAL_ENRICHMENT", "True").lower() == "true"
    ENABLE_AI_ENRICHMENT: bool = os.getenv("ENABLE_AI_ENRICHMENT", "True").lower() == "true"
    ENABLE_HUNTER_ENRICHMENT: bool = os.getenv("ENABLE_HUNTER_ENRICHMENT", "True").lower() == "true"
    ENABLE_CLEARBIT_ENRICHMENT: bool = os.getenv("ENABLE_CLEARBIT_ENRICHMENT", "True").lower() == "true"
    ENABLE_APOLLO_ENRICHMENT: bool = os.getenv("ENABLE_APOLLO_ENRICHMENT", "True").lower() == "true"
    
    # ==================== EMAIL VERIFICATION ====================
    EMAIL_VERIFICATION_ENABLED: bool = os.getenv("EMAIL_VERIFICATION_ENABLED", "True").lower() == "true"
    VERIFICATION_TIMEOUT: int = int(os.getenv("VERIFICATION_TIMEOUT", "10"))
    MAX_VERIFICATION_RETRIES: int = int(os.getenv("MAX_VERIFICATION_RETRIES", "3"))
    
    # ==================== LOGGING ====================
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "app.log")
    LOG_MAX_SIZE_MB: int = int(os.getenv("LOG_MAX_SIZE_MB", "10"))
    LOG_BACKUP_COUNT: int = int(os.getenv("LOG_BACKUP_COUNT", "5"))
    
    # ==================== GLOBAL CONSTANTS (Properties) ====================
    @property
    def COUNTRIES(self) -> List[Dict[str, Any]]:
        return GLOBAL_COUNTRIES
    
    @property
    def ETHIOPIAN_CONFIG(self) -> Dict[str, Any]:
        return ETHIOPIAN_CONFIG
    
    @property
    def INDUSTRY_HIERARCHY(self) -> Dict[str, Any]:
        return INDUSTRY_HIERARCHY
    
    @property
    def ALL_INDUSTRIES(self) -> List[str]:
        return ALL_INDUSTRIES
    
    @property
    def ICP_RULES(self) -> Dict[str, Any]:
        return ICP_RULES
    
    @property
    def SOURCES(self) -> List[Dict[str, Any]]:
        return SOURCES
    
    # ==================== API STATUS CHECK ====================
    @property
    def API_STATUS(self) -> dict:
        """Check which APIs are configured"""
        return {
            "newsapi": bool(self.NEWSAPI_KEY and "your_" not in self.NEWSAPI_KEY),
            "gnews": bool(self.GNEWS_KEY and "your_" not in self.GNEWS_KEY),
            "scrapingbee": bool(self.SCRAPINGBEE_KEY and "your_" not in self.SCRAPINGBEE_KEY),
            "scraperapi": bool(self.SCRAPERAPI_KEY and "your_" not in self.SCRAPERAPI_KEY),
            "alpha_vantage": bool(self.ALPHA_VANTAGE_KEY and "your_" not in self.ALPHA_VANTAGE_KEY),
            "finnhub": bool(self.FINNHUB_KEY and "your_" not in self.FINNHUB_KEY),
            "gemini": bool(self.GEMINI_API_KEY and "your_" not in self.GEMINI_API_KEY),
            "hunter": bool(self.HUNTER_API_KEY and "your_" not in self.HUNTER_API_KEY),
            "clearbit": bool(self.CLEARBIT_API_KEY and "your_" not in self.CLEARBIT_API_KEY),
            "apollo": bool(self.APOLLO_API_KEY and "your_" not in self.APOLLO_API_KEY),
            "exa": bool(self.EXA_API_KEY and "your_" not in self.EXA_API_KEY)
        }
    
    @property
    def SCRAPING_ENABLED(self) -> bool:
        """Check if web scraping is enabled and configured"""
        return self.ENABLE_REAL_SCRAPING and (bool(self.SCRAPINGBEE_KEY) or bool(self.SCRAPERAPI_KEY))
    
    @property
    def ENRICHMENT_ENABLED(self) -> bool:
        """Check if enrichment is enabled"""
        return any([
            self.ENABLE_HUNTER_ENRICHMENT and bool(self.HUNTER_API_KEY),
            self.ENABLE_CLEARBIT_ENRICHMENT and bool(self.CLEARBIT_API_KEY),
            self.ENABLE_APOLLO_ENRICHMENT and bool(self.APOLLO_API_KEY),
            self.ENABLE_AI_ENRICHMENT and bool(self.GEMINI_API_KEY),
            self.ENABLE_NEWS_ENRICHMENT
        ])
    
    # ==================== HELPER METHODS ====================
    def get_country_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        """Get country info by code"""
        for country in self.COUNTRIES:
            if country.get("code") == code:
                return country
        return None
    
    def get_country_name(self, code: str) -> str:
        """Get country name from code"""
        country = self.get_country_by_code(code)
        return country.get("name", code) if country else code
    
    def get_country_flag(self, code: str) -> str:
        """Get country flag emoji from code"""
        country = self.get_country_by_code(code)
        return country.get("flag", "🌍") if country else "🌍"
    
    def get_industries_by_category(self, category_name: str) -> List[str]:
        """Get industries for a specific category"""
        category = self.INDUSTRY_HIERARCHY.get(category_name)
        return category.get("industries", []) if category else []
    
    def get_all_categories(self) -> List[str]:
        """Get all industry category names"""
        return list(self.INDUSTRY_HIERARCHY.keys())
    
    def get_category_icon(self, category_name: str) -> str:
        """Get icon for a category"""
        category = self.INDUSTRY_HIERARCHY.get(category_name)
        return category.get("icon", "🏢") if category else "🏢"
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of the configuration"""
        api_status = self.API_STATUS
        return {
            "app_name": self.APP_NAME,
            "version": self.APP_VERSION,
            "environment": self.ENVIRONMENT,
            "host": self.HOST,
            "port": self.PORT,
            "database": self.MONGO_DB,
            "countries": len(self.COUNTRIES),
            "industries": len(self.ALL_INDUSTRIES),
            "industry_categories": len(self.INDUSTRY_HIERARCHY),
            "ethiopian_market": self.ETHIOPIAN_MARKET_ENABLED,
            "global_scraping": self.GLOBAL_SCRAPING_ENABLED,
            "apis_configured": sum(1 for v in api_status.values() if v),
            "api_status": api_status,
            "scraping_enabled": self.SCRAPING_ENABLED,
            "enrichment_enabled": self.ENRICHMENT_ENABLED
        }
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        arbitrary_types_allowed = True


# ==================== CREATE SINGLE INSTANCE ====================
settings = Settings()

# ==================== EXPORT FOR COMPATIBILITY ====================
# These are exported for backward compatibility with app.py
API_KEYS = {
    "newsapi": settings.NEWSAPI_KEY,
    "gnews": settings.GNEWS_KEY,
    "currents": settings.CURRENTS_API_KEY,
    "scrapingbee": settings.SCRAPINGBEE_KEY,
    "scraperapi": settings.SCRAPERAPI_KEY,
    "alpha_vantage": settings.ALPHA_VANTAGE_KEY,
    "finnhub": settings.FINNHUB_KEY,
    "gemini": settings.GEMINI_API_KEY,
    "hunter": settings.HUNTER_API_KEY,
    "clearbit": settings.CLEARBIT_API_KEY,
    "apollo": settings.APOLLO_API_KEY,
    "exa": settings.EXA_API_KEY
}

# ==================== PRINT CONFIGURATION STATUS ====================
if __name__ != "__main__":
    print("=" * 80)
    print("🌍 GLOBAL AI POWERED LEAD GENERATION SYSTEM")
    print("🇪🇹 ETHIOPIAN MARKET EDITION - v11.0")
    print("=" * 80)
    print(f"✅ Configuration loaded successfully")
    print(f"📊 App: {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"🌐 Environment: {settings.ENVIRONMENT}")
    print(f"🗄️  Database: {settings.MONGO_DB}")
    print(f"🌍 Server: http://{settings.HOST}:{settings.PORT}")
    print(f"🔗 CORS Origins: {settings.ALLOWED_ORIGINS}")
    print("=" * 80)
    
    # Country Status
    print(f"\n🌍 Countries Supported: {len(settings.COUNTRIES)}")
    print(f"   Default Countries: {', '.join(settings.DEFAULT_COUNTRIES)}")
    print(f"   Ethiopian Market: {'✅ ENABLED' if settings.ETHIOPIAN_MARKET_ENABLED else '⚠️ DISABLED'}")
    
    # Industry Status
    print(f"\n🏢 Industry Categories: {len(settings.INDUSTRY_HIERARCHY)}")
    print(f"   Total Industries: {len(settings.ALL_INDUSTRIES)}")
    for category in list(settings.INDUSTRY_HIERARCHY.keys())[:5]:
        icon = settings.INDUSTRY_HIERARCHY[category]['icon']
        count = len(settings.INDUSTRY_HIERARCHY[category]['industries'])
        print(f"   • {icon} {category}: {count} industries")
    if len(settings.INDUSTRY_HIERARCHY) > 5:
        print(f"   ... and {len(settings.INDUSTRY_HIERARCHY) - 5} more categories")
    
    # API Status
    api_status = settings.API_STATUS
    configured_apis = sum(1 for v in api_status.values() if v)
    print(f"\n🔑 APIs Configured: {configured_apis}/{len(api_status)}")
    for api, status in api_status.items():
        print(f"   • {api}: {'✅' if status else '❌'}")
    
    # Scraping & Enrichment Status
    print(f"\n🕷️  Real Web Scraping: {'✅ ENABLED' if settings.SCRAPING_ENABLED else '⚠️ DISABLED'}")
    print(f"📈 Enrichment: {'✅ ENABLED' if settings.ENRICHMENT_ENABLED else '⚠️ DISABLED'}")
    print(f"⚡ Concurrent Scrapers: {settings.CONCURRENT_SCRAPERS}")
    print("=" * 80)

# ==================== TEST CONFIGURATION ====================
if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("CONFIGURATION TEST")
    print("=" * 80)
    
    print(f"\n📊 Application Settings:")
    print(f"  Name: {settings.APP_NAME}")
    print(f"  Version: {settings.APP_VERSION}")
    print(f"  Environment: {settings.ENVIRONMENT}")
    print(f"  Host: {settings.HOST}:{settings.PORT}")
    
    print(f"\n🌍 Global Settings:")
    print(f"  Countries: {len(settings.COUNTRIES)}")
    print(f"  First 5 Countries:")
    for country in settings.COUNTRIES[:5]:
        print(f"    {country['flag']} {country['code']} - {country['name']}")
    
    print(f"\n🏢 Industry Settings:")
    print(f"  Categories: {len(settings.INDUSTRY_HIERARCHY)}")
    print(f"  Total Industries: {len(settings.ALL_INDUSTRIES)}")
    
    print(f"\n🇪🇹 Ethiopian Market:")
    print(f"  Enabled: {settings.ETHIOPIAN_MARKET_ENABLED}")
    print(f"  Regions: {len(settings.ETHIOPIAN_CONFIG['regions'])}")
    print(f"  Cities: {len(settings.ETHIOPIAN_CONFIG['cities'])}")
    print(f"  Directories: {len(settings.ETHIOPIAN_CONFIG['directories'])}")
    
    print(f"\n🔑 API Keys Status:")
    for api, status in settings.API_STATUS.items():
        print(f"  {api}: {'✅' if status else '❌'}")
    
    print(f"\n📋 ICP Rules:")
    print(f"  Target Industries: {len(settings.ICP_RULES['industries'])}")
    print(f"  Employees: {settings.ICP_RULES['min_employees']}-{settings.ICP_RULES['max_employees']}")
    print(f"  Target Roles: {len(settings.ICP_RULES['target_roles'])}")
    
    print(f"\n🗄️ Database:")
    print(f"  Name: {settings.MONGO_DB}")
    print(f"  URI: {'[SET]' if settings.MONGODB_URI else '[MISSING]'}")
    
    print(f"\n✅ Configuration test completed successfully!")
    print("=" * 80)