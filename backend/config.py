# backend/config.py - Global AI Powered Lead Generation System Configuration
"""
Configuration module for Global AI Powered Lead Generation System.
Centralizes all configuration settings with support for:
- 50+ Countries
- Advanced Industry Hierarchy (15 categories, 150+ industries)
- Ethiopian Market Integration
- Multiple API Integrations
- Dynamic Feature Flags
"""

import os
import sys
import json
from typing import List, Dict, Any, Optional, Union
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

# Try to import Pydantic settings, fallback to simple config if not available
try:
    from pydantic import Field, validator
    from pydantic_settings import BaseSettings
    USE_PYDANTIC = True
except ImportError:
    USE_PYDANTIC = False
    print("⚠️  pydantic-settings not found. Using simple configuration.")

# ==================== HELPER FUNCTIONS ====================
def parse_json_list(value: Union[str, List]) -> List:
    """Parse a JSON list from string or return as-is"""
    if isinstance(value, str):
        value = value.strip()
        if value.startswith('[') and value.endswith(']'):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass
        if ',' in value:
            return [item.strip() for item in value.split(',')]
        return [value] if value else []
    return value or []

def parse_json_dict(value: Union[str, Dict]) -> Dict:
    """Parse a JSON dict from string or return as-is"""
    if isinstance(value, str):
        value = value.strip()
        if value.startswith('{') and value.endswith('}'):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass
    return value or {}

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
        {"code": "CO", "name": "Colombia", "flag": "🇨🇴"},
        {"code": "PE", "name": "Peru", "flag": "🇵🇪"},
        {"code": "VE", "name": "Venezuela", "flag": "🇻🇪"},
        {"code": "RU", "name": "Russia", "flag": "🇷🇺"},
        {"code": "TR", "name": "Turkey", "flag": "🇹🇷"},
        {"code": "PK", "name": "Pakistan", "flag": "🇵🇰"},
        {"code": "BD", "name": "Bangladesh", "flag": "🇧🇩"},
        {"code": "NG", "name": "Nigeria", "flag": "🇳🇬"},
        {"code": "TZ", "name": "Tanzania", "flag": "🇹🇿"},
        {"code": "UG", "name": "Uganda", "flag": "🇺🇬"},
        {"code": "RW", "name": "Rwanda", "flag": "🇷🇼"}
    ],
    "regions": {
        "ET": ["Addis Ababa", "Oromia", "Amhara", "Tigray", "Sidama", "SNNPR", "Gambela", 
               "Benishangul-Gumuz", "Somali", "Afar", "Harari", "Dire Dawa"],
        "US": ["California", "Texas", "Florida", "New York", "Illinois", "Pennsylvania", 
               "Ohio", "Georgia", "North Carolina", "Michigan", "New Jersey", "Virginia", 
               "Washington", "Arizona", "Massachusetts", "Tennessee", "Indiana", "Missouri", 
               "Maryland", "Wisconsin", "Colorado", "Minnesota", "South Carolina", "Alabama", 
               "Louisiana", "Kentucky", "Oregon", "Oklahoma", "Connecticut", "Utah", "Iowa", 
               "Nevada", "Arkansas", "Mississippi", "Kansas", "New Mexico", "Nebraska", 
               "West Virginia", "Idaho", "Hawaii", "Maine", "New Hampshire", "Rhode Island", 
               "Montana", "Delaware", "South Dakota", "North Dakota", "Vermont", "Wyoming", "Alaska"],
        "GB": ["England", "Scotland", "Wales", "Northern Ireland", "London", "Greater Manchester", 
               "West Midlands", "West Yorkshire", "Merseyside", "South Yorkshire"],
        "CA": ["Ontario", "Quebec", "British Columbia", "Alberta", "Manitoba", "Saskatchewan", 
               "Nova Scotia", "New Brunswick", "Newfoundland", "Prince Edward Island"],
        "AU": ["New South Wales", "Victoria", "Queensland", "Western Australia", "South Australia", 
               "Tasmania", "Australian Capital Territory", "Northern Territory"],
        "DE": ["Berlin", "Bavaria", "Hamburg", "North Rhine-Westphalia", "Lower Saxony", "Hesse", 
               "Baden-Württemberg", "Saxony", "Thuringia", "Rhineland-Palatinate"],
        "FR": ["Île-de-France", "Auvergne-Rhône-Alpes", "Grand Est", "Nouvelle-Aquitaine", 
               "Occitanie", "Hauts-de-France", "Provence-Alpes-Côte d'Azur", "Brittany", 
               "Normandy", "Centre-Val de Loire"],
        "IT": ["Lombardy", "Lazio", "Campania", "Veneto", "Piedmont", "Emilia-Romagna", "Tuscany", 
               "Sicily", "Apulia", "Liguria", "Marche", "Abruzzo"],
        "ES": ["Andalusia", "Catalonia", "Community of Madrid", "Valencia", "Castile and León", 
               "Basque Country", "Aragon", "Murcia", "Balearic Islands", "Canary Islands"],
        "IN": ["Maharashtra", "Uttar Pradesh", "Tamil Nadu", "Karnataka", "Gujarat", "Rajasthan", 
               "West Bengal", "Delhi", "Telangana", "Andhra Pradesh", "Kerala", "Punjab"],
        "CN": ["Beijing", "Shanghai", "Guangdong", "Zhejiang", "Jiangsu", "Sichuan", "Hubei", 
               "Shandong", "Henan", "Fujian", "Hunan", "Anhui"],
        "JP": ["Tokyo", "Osaka", "Kanagawa", "Aichi", "Hokkaido", "Fukuoka", "Kyoto", "Hyogo", 
               "Saitama", "Chiba", "Hiroshima", "Miyagi"],
        "BR": ["São Paulo", "Rio de Janeiro", "Minas Gerais", "Rio Grande do Sul", "Bahia", 
               "Paraná", "Pernambuco", "Ceará", "Santa Catarina", "Goiás", "Amazonas"],
        "KE": ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Thika", "Malindi", "Naivasha"],
        "NG": ["Lagos", "Abuja", "Kano", "Port Harcourt", "Ibadan", "Kaduna", "Enugu", "Aba"],
        "ZA": ["Gauteng", "Western Cape", "KwaZulu-Natal", "Eastern Cape", "Free State", 
               "Mpumalanga", "Limpopo", "North West", "Northern Cape"]
    },
    "cities": {
        "ET": ["Addis Ababa", "Adama", "Bahir Dar", "Gondar", "Mekelle", "Hawassa", "Jimma", 
               "Dire Dawa", "Dessie", "Jijiga", "Shashamane", "Bishoftu", "Arba Minch", "Hosaena", 
               "Wolaita Sodo", "Gambela", "Assosa", "Semera", "Harar", "Debre Birhan", "Debre Markos", 
               "Kombolcha", "Adigrat", "Axum", "Lalibela"],
        "US": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", 
               "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "Fort Worth", "Columbus", 
               "Charlotte", "San Francisco", "Indianapolis", "Seattle", "Denver", "Washington DC", 
               "Boston", "Miami", "Atlanta", "Portland", "Las Vegas", "Detroit", "Memphis", "Louisville"],
        "GB": ["London", "Birmingham", "Leeds", "Glasgow", "Manchester", "Sheffield", "Bradford", 
               "Edinburgh", "Liverpool", "Bristol", "Cardiff", "Belfast", "Newcastle", "Nottingham", 
               "Southampton", "Portsmouth", "Aberdeen", "Swansea"],
        "CA": ["Toronto", "Montreal", "Vancouver", "Calgary", "Edmonton", "Ottawa", "Winnipeg", 
               "Quebec City", "Hamilton", "Halifax", "Mississauga", "Brampton", "Surrey", "Laval"],
        "AU": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Gold Coast", "Newcastle", 
               "Canberra", "Hobart", "Wollongong", "Sunshine Coast", "Geelong"],
        "DE": ["Berlin", "Hamburg", "Munich", "Cologne", "Frankfurt", "Stuttgart", "Düsseldorf", 
               "Dortmund", "Essen", "Leipzig", "Bremen", "Dresden", "Hannover", "Nuremberg"],
        "FR": ["Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpellier", 
               "Bordeaux", "Lille", "Rennes", "Reims", "Le Havre", "Saint-Étienne"],
        "IT": ["Rome", "Milan", "Naples", "Turin", "Palermo", "Genoa", "Bologna", "Florence", "Bari", 
               "Catania", "Venice", "Verona", "Messina", "Padua", "Trieste"],
        "ES": ["Madrid", "Barcelona", "Valencia", "Seville", "Zaragoza", "Málaga", "Murcia", "Palma", 
               "Bilbao", "Alicante", "Córdoba", "Valladolid", "Vigo", "Gijón"],
        "IN": ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Ahmedabad", "Chennai", "Kolkata", "Pune", 
               "Jaipur", "Lucknow", "Nagpur", "Indore", "Bhopal", "Visakhapatnam", "Patna"],
        "CN": ["Beijing", "Shanghai", "Shenzhen", "Guangzhou", "Chengdu", "Hangzhou", "Wuhan", "Nanjing", 
               "Tianjin", "Chongqing", "Xi'an", "Suzhou", "Dalian", "Qingdao", "Harbin"],
        "JP": ["Tokyo", "Yokohama", "Osaka", "Nagoya", "Sapporo", "Fukuoka", "Kobe", "Kyoto", "Saitama", 
               "Hiroshima", "Sendai", "Chiba", "Kitakyushu", "Sakai", "Niigata"],
        "BR": ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Fortaleza", "Belo Horizonte", 
               "Manaus", "Curitiba", "Recife", "Porto Alegre", "Goiânia", "Belém", "Guarulhos"],
        "KE": ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Thika", "Malindi", "Naivasha", "Meru"],
        "NG": ["Lagos", "Abuja", "Kano", "Port Harcourt", "Ibadan", "Kaduna", "Enugu", "Aba", "Maiduguri"],
        "ZA": ["Cape Town", "Johannesburg", "Pretoria", "Durban", "Port Elizabeth", "Bloemfontein", 
               "East London", "Nelspruit", "Kimberley", "Pietermaritzburg"]
    }
}

# ==================== ADVANCED INDUSTRY HIERARCHY ====================
INDUSTRY_HIERARCHY = {
    'Technology & Software': {
        'icon': '💻',
        'industries': [
            'Software Development', 'SaaS', 'Cloud Computing', 'Artificial Intelligence', 
            'Machine Learning', 'Blockchain', 'Cybersecurity', 'Data Analytics', 
            'FinTech', 'EdTech', 'HealthTech', 'PropTech', 'LegalTech', 
            'HR Tech', 'AdTech', 'MarTech', 'InsurTech', 'AgriTech',
            'Quantum Computing', 'AR/VR', 'IoT', 'Robotics'
        ]
    },
    'E-commerce & Retail': {
        'icon': '🛒',
        'industries': [
            'E-commerce', 'Retail', 'D2C Brands', 'Marketplace', 
            'CPG', 'FMCG', 'Consumer Goods', 'Fashion & Apparel', 
            'Luxury Goods', 'Beauty & Cosmetics', 'Jewelry', 'Sports & Outdoors',
            'Omnichannel Retail', 'Dropshipping', 'Subscription Box'
        ]
    },
    'Finance & Banking': {
        'icon': '💰',
        'industries': [
            'Banking', 'Investment Banking', 'Asset Management', 'Private Equity', 
            'Venture Capital', 'Hedge Funds', 'Insurance', 'Real Estate Investment', 
            'Commercial Banking', 'Retail Banking', 'Microfinance', 'Islamic Banking',
            'Wealth Management', 'Crypto Finance', 'Digital Banking'
        ]
    },
    'Healthcare & Life Sciences': {
        'icon': '🏥',
        'industries': [
            'Healthcare', 'Hospitals', 'Pharmaceuticals', 'Biotechnology', 
            'Medical Devices', 'Telemedicine', 'Health Insurance', 
            'Mental Health', 'Senior Care', 'Veterinary', 'Clinical Research',
            'Dental Care', 'Optometry', 'Physical Therapy'
        ]
    },
    'Manufacturing & Industrial': {
        'icon': '🏭',
        'industries': [
            'Manufacturing', 'Industrial', 'Automotive', 'Aerospace', 
            'Construction', 'Steel & Metals', 'Textiles', 'Chemical', 
            'Plastics', 'Electronics Manufacturing', 'Paper & Packaging',
            '3D Printing', 'Additive Manufacturing', 'Industrial Automation',
            'Heavy Machinery', 'Defense Manufacturing'
        ]
    },
    'Energy & Utilities': {
        'icon': '⚡',
        'industries': [
            'Renewable Energy', 'Oil & Gas', 'Solar Energy', 'Wind Energy', 
            'Utilities', 'Water Management', 'Nuclear Energy', 'Energy Storage',
            'Geothermal', 'Hydroelectric', 'Smart Grid', 'Carbon Capture'
        ]
    },
    'Agriculture & Food': {
        'icon': '🌾',
        'industries': [
            'Agriculture', 'Coffee Export', 'Flower Farming', 'Food Processing', 
            'Farming', 'Agribusiness', 'Fisheries', 'Forestry', 
            'Organic Farming', 'Sustainable Agriculture', 'AgTech',
            'Food Manufacturing', 'Beverage Production', 'Cannabis Cultivation'
        ]
    },
    'Transportation & Logistics': {
        'icon': '🚚',
        'industries': [
            'Logistics', 'Transportation', 'Shipping', 'Aviation', 
            'Railway', 'Supply Chain', 'Warehousing', 'Fleet Management', 
            'Last Mile Delivery', 'Maritime', 'Freight Forwarding',
            'Autonomous Vehicles', 'Drone Delivery', 'Port Management'
        ]
    },
    'Real Estate & Construction': {
        'icon': '🏗️',
        'industries': [
            'Real Estate', 'Construction', 'Architecture', 'Urban Planning', 
            'Property Management', 'Real Estate Development', 'Interior Design',
            'Landscaping', 'Civil Engineering', 'Smart Buildings'
        ]
    },
    'Media & Entertainment': {
        'icon': '🎬',
        'industries': [
            'Media', 'Entertainment', 'Publishing', 'Broadcasting', 
            'Film Production', 'Music', 'Gaming', 'Digital Media', 
            'Streaming Services', 'Podcasting', 'Animation', 
            'VFX', 'Game Development', 'Esports'
        ]
    },
    'Telecommunications': {
        'icon': '📡',
        'industries': [
            'Telecom', 'Mobile Networks', 'Broadband', 'Satellite', 
            'Internet Service', '5G Technology', 'IoT Infrastructure',
            'Network Equipment', 'Fibre Optic', 'Wireless Communication'
        ]
    },
    'Education & Training': {
        'icon': '📚',
        'industries': [
            'Education', 'EdTech', 'Training', 'Higher Education', 
            'K-12 Schools', 'Online Learning', 'Corporate Training', 
            'Vocational Training', 'Language Schools', 'Test Preparation',
            'Special Education', 'Tutoring Services'
        ]
    },
    'Professional Services': {
        'icon': '💼',
        'industries': [
            'Consulting', 'Legal Services', 'Accounting', 'Architecture', 
            'Engineering', 'HR Services', 'Marketing Agency', 'PR Agency', 
            'Recruitment', 'Outsourcing', 'Management Consulting',
            'IT Consulting', 'Strategy Consulting', 'Tax Services',
            'Audit Services', 'Executive Search'
        ]
    },
    'Hospitality & Tourism': {
        'icon': '🏨',
        'industries': [
            'Hospitality', 'Tourism', 'Hotels', 'Restaurants', 
            'Travel Agencies', 'Cruise Lines', 'Tour Operators', 
            'Catering', 'Event Management', 'Theme Parks',
            'Resorts', 'Spa Services', 'Casinos'
        ]
    },
    'Non-Profit & Social': {
        'icon': '❤️',
        'industries': [
            'Non-Profit', 'NGO', 'Social Enterprise', 'Charity', 
            'Foundations', 'Community Development', 'Human Rights', 
            'Environmental', 'Animal Welfare', 'Cultural Heritage',
            'Religious Organizations', 'Public Health'
        ]
    }
}

# Flattened industry list for filters
ALL_INDUSTRIES = []
for category in INDUSTRY_HIERARCHY.values():
    ALL_INDUSTRIES.extend(category['industries'])

# ==================== API KEYS ====================
API_KEYS = {
    "newsapi": os.getenv("NEWSAPI_KEY", ""),
    "gnews": os.getenv("GNEWS_KEY", ""),
    "currents": os.getenv("CURRENTS_API_KEY", ""),
    "scrapingbee": os.getenv("SCRAPINGBEE_KEY", ""),
    "scraperapi": os.getenv("SCRAPERAPI_KEY", ""),
    "alpha_vantage": os.getenv("ALPHA_VANTAGE_KEY", ""),
    "finnhub": os.getenv("FINNHUB_KEY", ""),
    "gemini": os.getenv("GEMINI_API_KEY", ""),
    "apollo": os.getenv("APOLLO_API_KEY", ""),
    "clearbit": os.getenv("CLEARBIT_API_KEY", ""),
    "hunter": os.getenv("HUNTER_API_KEY", "de596313be4c55fc23494dee2e0bb78816ff6485"),
    "exa": os.getenv("EXA_API_KEY", ""),
    "builtwith": os.getenv("BUILTWITH_API_KEY", ""),
    "peopledatalabs": os.getenv("PDL_API_KEY", ""),
    "linkedin": os.getenv("LINKEDIN_API_KEY", ""),
    "crunchbase": os.getenv("CRUNCHBASE_API_KEY", ""),
    "indeed": os.getenv("INDEED_API_KEY", "")
}

# ==================== ICP CONFIGURATION ====================
ICP_RULES = {
    "industries": os.getenv("ICP_INDUSTRIES", "technology,software,saas,fintech,marketing,advertising,consulting,design,coffee export,textile,manufacturing,banking").split(","),
    "min_employees": int(os.getenv("ICP_MIN_EMPLOYEES", "10")),
    "max_employees": int(os.getenv("ICP_MAX_EMPLOYEES", "500")),
    "min_founded": int(os.getenv("ICP_MIN_FOUNDED", "2015")),
    "target_roles": os.getenv("ICP_TARGET_ROLES", "CEO,CTO,CMO,Founder,Marketing Director,Head of Sales,Managing Director,General Manager").split(","),
    "funding_stages": os.getenv("ICP_FUNDING_STAGES", "seed,series_a,series_b").split(",")
}

# ==================== ETHIOPIAN CONFIGURATION ====================
ETHIOPIAN_CONFIG = {
    "regions": GLOBAL_CONFIG["regions"]["ET"],
    "cities": GLOBAL_CONFIG["cities"]["ET"],
    "industries": ALL_INDUSTRIES,
    "directories": [
        "2ehire.com",
        "ethioyellowpages.com",
        "ethiobusiness.net",
        "ethiopianbusiness.net",
        "addischamber.org",
        "ethiopianchamber.com",
        "ethiocompanies.com",
        "2merkato.com"
    ],
    "business_types": [
        "Share Company",
        "Private Limited Company",
        "Public Enterprise",
        "Sole Proprietorship",
        "Partnership",
        "Cooperative"
    ]
}

# ==================== SOURCE CONFIGURATION ====================
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

if USE_PYDANTIC:
    # ==================== PYDANTIC SETTINGS ====================
    class Settings(BaseSettings):
        """
        Application settings using Pydantic BaseSettings.
        Environment variables take precedence over default values.
        """
        
        # Application Settings
        APP_NAME: str = Field(default="Global AI Powered Lead Generation System", env="APP_NAME")
        APP_VERSION: str = Field(default="11.0.0", env="APP_VERSION")
        DEBUG: bool = Field(default=True, env="DEBUG")
        HOST: str = Field(default="0.0.0.0", env="HOST")
        PORT: int = Field(default=8007, env="PORT")
        API_PREFIX: str = Field(default="/api", env="API_PREFIX")
        
        # CORS Settings
        CORS_ORIGINS: List[str] = Field(
            default=["http://localhost:3000", "http://localhost:8007", "http://127.0.0.1:8007", "*"],
            env="CORS_ORIGINS"
        )
        
        # Database Settings
        MONGODB_URI: str = Field(
            default="mongodb://localhost:27017",
            env="MONGODB_URI"
        )
        DATABASE_NAME: str = Field(
            default="agency_intel",
            env="DATABASE_NAME"
        )
        
        # Feature Flags
        GLOBAL_SCRAPING_ENABLED: bool = Field(default=True, env="GLOBAL_SCRAPING_ENABLED")
        ETHIOPIAN_MARKET_ENABLED: bool = Field(default=True, env="ETHIOPIAN_MARKET_ENABLED")
        AUTO_SCORING_ENABLED: bool = Field(default=True, env="AUTO_SCORING_ENABLED")
        AI_DESCRIPTIONS_ENABLED: bool = Field(default=True, env="AI_DESCRIPTIONS_ENABLED")
        
        # Scraping Settings
        MAX_LEADS_PER_SCRAPE: int = Field(default=1000, env="MAX_LEADS_PER_SCRAPE")
        SCRAPE_TIMEOUT_SECONDS: int = Field(default=300, env="SCRAPE_TIMEOUT_SECONDS")
        CONCURRENT_SCRAPERS: int = Field(default=5, env="CONCURRENT_SCRAPERS")
        RATE_LIMIT_DELAY: float = Field(default=1.0, env="RATE_LIMIT_DELAY")
        
        # Email Verification Settings
        EMAIL_VERIFICATION_ENABLED: bool = Field(default=True, env="EMAIL_VERIFICATION_ENABLED")
        VERIFICATION_TIMEOUT: int = Field(default=10, env="VERIFICATION_TIMEOUT")
        MAX_VERIFICATION_RETRIES: int = Field(default=3, env="MAX_VERIFICATION_RETRIES")
        
        # Scoring Configuration
        SCORING_WEIGHTS_JSON: str = Field(
            default='{"hiring_signal": 0.25, "funding_signal": 0.30, "tech_refresh_signal": 0.20, "expansion_signal": 0.15, "leadership_change_signal": 0.10}',
            env="SCORING_WEIGHTS"
        )
        PRIORITY_THRESHOLDS_JSON: str = Field(
            default='{"hot": 80, "warm": 60, "cold": 40, "excluded": 0}',
            env="PRIORITY_THRESHOLDS"
        )
        
        # Global Configuration (read-only properties)
        @property
        def COUNTRIES(self) -> List[Dict[str, Any]]:
            return GLOBAL_CONFIG["countries"]
        
        @property
        def REGIONS(self) -> Dict[str, List[str]]:
            return GLOBAL_CONFIG["regions"]
        
        @property
        def CITIES(self) -> Dict[str, List[str]]:
            return GLOBAL_CONFIG["cities"]
        
        @property
        def INDUSTRY_HIERARCHY(self) -> Dict[str, Dict[str, Any]]:
            return INDUSTRY_HIERARCHY
        
        @property
        def ALL_INDUSTRIES(self) -> List[str]:
            return ALL_INDUSTRIES
        
        @property
        def API_KEYS(self) -> Dict[str, str]:
            return API_KEYS
        
        @property
        def ICP_RULES(self) -> Dict[str, Any]:
            return ICP_RULES
        
        @property
        def ETHIOPIAN_CONFIG(self) -> Dict[str, Any]:
            return ETHIOPIAN_CONFIG
        
        @property
        def SOURCES(self) -> List[Dict[str, Any]]:
            return SOURCES
        
        # Validators
        @validator("CORS_ORIGINS", pre=True)
        def parse_cors_origins(cls, v):
            return parse_json_list(v)
        
        @validator("SCORING_WEIGHTS_JSON", pre=True)
        def parse_scoring_weights(cls, v):
            if isinstance(v, dict):
                return json.dumps(v)
            return v
        
        @validator("PRIORITY_THRESHOLDS_JSON", pre=True)
        def parse_priority_thresholds(cls, v):
            if isinstance(v, dict):
                return json.dumps(v)
            return v
        
        @validator("MONGODB_URI")
        def validate_mongodb_uri(cls, v):
            if not v:
                raise ValueError("MONGODB_URI must be set")
            return v
        
        @validator("DATABASE_NAME")
        def validate_database_name(cls, v):
            if not v:
                raise ValueError("DATABASE_NAME must be set")
            return v
        
        # Computed properties
        @property
        def SCORING_WEIGHTS(self) -> Dict[str, float]:
            return json.loads(self.SCORING_WEIGHTS_JSON)
        
        @property
        def PRIORITY_THRESHOLDS(self) -> Dict[str, int]:
            return json.loads(self.PRIORITY_THRESHOLDS_JSON)
        
        # API Integration Settings
        @property
        def API_INTEGRATIONS(self) -> Dict[str, Dict[str, Any]]:
            return {
                "clearbit": {
                    "enabled": bool(self.API_KEYS.get("clearbit")),
                    "api_key": self.API_KEYS.get("clearbit", ""),
                    "enrich_company_data": True,
                    "enrich_person_data": True
                },
                "hunter": {
                    "enabled": bool(self.API_KEYS.get("hunter")),
                    "api_key": self.API_KEYS.get("hunter", ""),
                    "domain_search": True,
                    "email_finder": True,
                    "email_verifier": True,
                    "company_enrichment": True,
                    "person_enrichment": True
                },
                "apollo": {
                    "enabled": bool(self.API_KEYS.get("apollo")),
                    "api_key": self.API_KEYS.get("apollo", ""),
                    "find_contacts": True,
                    "company_search": True
                },
                "exa": {
                    "enabled": bool(self.API_KEYS.get("exa")),
                    "api_key": self.API_KEYS.get("exa", ""),
                    "company_search": True
                },
                "gemini": {
                    "enabled": bool(self.API_KEYS.get("gemini")),
                    "api_key": self.API_KEYS.get("gemini", ""),
                    "generate_descriptions": True
                }
            }
        
        # Logging Configuration
        @property
        def LOGGING_CONFIG(self) -> Dict[str, Any]:
            return {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": "app.log",
                "max_size_mb": 10,
                "backup_count": 5
            }
        
        # Security Settings
        @property
        def SECURITY(self) -> Dict[str, Any]:
            return {
                "secret_key": os.getenv("SECRET_KEY", "your-secret-key-change-in-production"),
                "algorithm": "HS256",
                "access_token_expire_minutes": 30,
                "refresh_token_expire_days": 7
            }
        
        model_config = {
            "env_file": ".env",
            "env_file_encoding": "utf-8",
            "case_sensitive": False,
            "extra": "ignore"
        }
    
    # Create config instance
    config = Settings()

else:
    # ==================== SIMPLE CONFIGURATION (Fallback) ====================
    class SimpleConfig:
        """Simple configuration class without Pydantic dependencies"""
        
        # Application Settings
        APP_NAME = "Global AI Powered Lead Generation System"
        APP_VERSION = "11.0.0"
        DEBUG = os.getenv("DEBUG", "True").lower() == "true"
        HOST = os.getenv("HOST", "0.0.0.0")
        PORT = int(os.getenv("PORT", "8007"))
        API_PREFIX = "/api"
        
        # Feature Flags
        GLOBAL_SCRAPING_ENABLED = os.getenv("GLOBAL_SCRAPING_ENABLED", "True").lower() == "true"
        ETHIOPIAN_MARKET_ENABLED = os.getenv("ETHIOPIAN_MARKET_ENABLED", "True").lower() == "true"
        AUTO_SCORING_ENABLED = os.getenv("AUTO_SCORING_ENABLED", "True").lower() == "true"
        AI_DESCRIPTIONS_ENABLED = os.getenv("AI_DESCRIPTIONS_ENABLED", "True").lower() == "true"
        
        # Scraping Settings
        MAX_LEADS_PER_SCRAPE = int(os.getenv("MAX_LEADS_PER_SCRAPE", "1000"))
        SCRAPE_TIMEOUT_SECONDS = int(os.getenv("SCRAPE_TIMEOUT_SECONDS", "300"))
        CONCURRENT_SCRAPERS = int(os.getenv("CONCURRENT_SCRAPERS", "5"))
        RATE_LIMIT_DELAY = float(os.getenv("RATE_LIMIT_DELAY", "1.0"))
        
        # Email Verification
        EMAIL_VERIFICATION_ENABLED = os.getenv("EMAIL_VERIFICATION_ENABLED", "True").lower() == "true"
        VERIFICATION_TIMEOUT = int(os.getenv("VERIFICATION_TIMEOUT", "10"))
        MAX_VERIFICATION_RETRIES = int(os.getenv("MAX_VERIFICATION_RETRIES", "3"))
        
        # Database Settings
        MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        DATABASE_NAME = os.getenv("DATABASE_NAME", "agency_intel")
        
        # CORS Settings
        @property
        def CORS_ORIGINS(self):
            value = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8007,http://127.0.0.1:8007,*")
            return parse_json_list(value)
        
        # Scoring Configuration
        @property
        def SCORING_WEIGHTS(self):
            value = os.getenv("SCORING_WEIGHTS", '{"hiring_signal": 0.25, "funding_signal": 0.30, "tech_refresh_signal": 0.20, "expansion_signal": 0.15, "leadership_change_signal": 0.10}')
            parsed = parse_json_dict(value)
            if isinstance(parsed, dict):
                return parsed
            return {"hiring_signal": 0.25, "funding_signal": 0.30, "tech_refresh_signal": 0.20, "expansion_signal": 0.15, "leadership_change_signal": 0.10}
        
        @property
        def PRIORITY_THRESHOLDS(self):
            value = os.getenv("PRIORITY_THRESHOLDS", '{"hot": 80, "warm": 60, "cold": 40, "excluded": 0}')
            parsed = parse_json_dict(value)
            if isinstance(parsed, dict):
                return parsed
            return {"hot": 80, "warm": 60, "cold": 40, "excluded": 0}
        
        # Global Configuration (read-only properties)
        @property
        def COUNTRIES(self):
            return GLOBAL_CONFIG["countries"]
        
        @property
        def REGIONS(self):
            return GLOBAL_CONFIG["regions"]
        
        @property
        def CITIES(self):
            return GLOBAL_CONFIG["cities"]
        
        @property
        def INDUSTRY_HIERARCHY(self):
            return INDUSTRY_HIERARCHY
        
        @property
        def ALL_INDUSTRIES(self):
            return ALL_INDUSTRIES
        
        @property
        def API_KEYS(self):
            return API_KEYS
        
        @property
        def ICP_RULES(self):
            return ICP_RULES
        
        @property
        def ETHIOPIAN_CONFIG(self):
            return ETHIOPIAN_CONFIG
        
        @property
        def SOURCES(self):
            return SOURCES
        
        @property
        def API_INTEGRATIONS(self):
            return {
                "clearbit": {
                    "enabled": bool(self.API_KEYS.get("clearbit")),
                    "api_key": self.API_KEYS.get("clearbit", ""),
                    "enrich_company_data": True
                },
                "hunter": {
                    "enabled": bool(self.API_KEYS.get("hunter")),
                    "api_key": self.API_KEYS.get("hunter", ""),
                    "domain_search": True,
                    "email_verifier": True,
                    "company_enrichment": True
                },
                "apollo": {
                    "enabled": bool(self.API_KEYS.get("apollo")),
                    "api_key": self.API_KEYS.get("apollo", "")
                },
                "gemini": {
                    "enabled": bool(self.API_KEYS.get("gemini")),
                    "api_key": self.API_KEYS.get("gemini", ""),
                    "generate_descriptions": True
                }
            }
        
        @property
        def LOGGING_CONFIG(self):
            return {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": "app.log"
            }
        
        @property
        def SECURITY(self):
            return {
                "secret_key": os.getenv("SECRET_KEY", "your-secret-key-change-in-production"),
                "algorithm": "HS256"
            }
    
    # Create config instance
    config = SimpleConfig()

# ==================== HELPER FUNCTIONS ====================
def get_config_dict() -> Dict[str, Any]:
    """Get all configuration as a dictionary (excluding sensitive data)"""
    config_dict = {}
    for key in dir(config):
        if not key.startswith('_') and not key.islower():
            try:
                value = getattr(config, key)
                if not callable(value):
                    config_dict[key] = value
            except:
                pass
    
    # Remove sensitive data
    sensitive_keys = ["password", "secret", "key", "uri", "token"]
    for key in list(config_dict.keys()):
        value = config_dict[key]
        if any(sensitive in key.lower() for sensitive in sensitive_keys):
            config_dict[key] = "[REDACTED]"
        elif isinstance(value, dict):
            for sub_key in list(value.keys()):
                if any(sensitive in str(sub_key).lower() for sensitive in sensitive_keys):
                    value[sub_key] = "[REDACTED]"
    return config_dict

def validate_configuration() -> bool:
    """Validate configuration on startup"""
    validation_errors = []
    
    if not config.MONGODB_URI:
        validation_errors.append("MONGODB_URI must be set")
    if not config.DATABASE_NAME:
        validation_errors.append("DATABASE_NAME must be set")
    
    if hasattr(config, 'SCORING_WEIGHTS'):
        total_weight = sum(config.SCORING_WEIGHTS.values())
        if abs(total_weight - 1.0) > 0.01:
            validation_errors.append(f"SCORING_WEIGHTS should sum to 1.0, got {total_weight:.2f}")
    
    if validation_errors:
        print("⚠️ Configuration validation errors:")
        for error in validation_errors:
            print(f"  - {error}")
        return False
    return True

def is_development() -> bool:
    return config.DEBUG

def is_production() -> bool:
    return not config.DEBUG

def get_api_url() -> str:
    return f"http://{config.HOST}:{config.PORT}{config.API_PREFIX}"

def get_database_url() -> str:
    return f"{config.MONGODB_URI}/{config.DATABASE_NAME}"

def get_config_summary() -> Dict[str, Any]:
    return {
        "app_name": config.APP_NAME,
        "version": config.APP_VERSION,
        "environment": "development" if config.DEBUG else "production",
        "host": config.HOST,
        "port": config.PORT,
        "database": config.DATABASE_NAME,
        "countries": len(config.COUNTRIES),
        "industries": len(config.ALL_INDUSTRIES),
        "industry_categories": len(config.INDUSTRY_HIERARCHY),
        "ethiopian_market": config.ETHIOPIAN_MARKET_ENABLED,
        "global_scraping": config.GLOBAL_SCRAPING_ENABLED,
        "api_integrations": list(config.API_INTEGRATIONS.keys())
    }

def get_country_by_code(country_code: str) -> Optional[Dict[str, Any]]:
    """Get country info by code"""
    for country in config.COUNTRIES:
        if country.get("code") == country_code:
            return country
    return None

def get_country_name(code: str) -> str:
    """Get country name from code"""
    country = get_country_by_code(code)
    return country.get("name", code) if country else code

def get_country_flag(code: str) -> str:
    """Get country flag emoji from code"""
    country = get_country_by_code(code)
    return country.get("flag", "🌍") if country else "🌍"

def get_industries_by_category(category_name: str) -> List[str]:
    """Get industries for a specific category"""
    category = config.INDUSTRY_HIERARCHY.get(category_name)
    return category.get("industries", []) if category else []

def get_all_categories() -> List[str]:
    """Get all industry category names"""
    return list(config.INDUSTRY_HIERARCHY.keys())

def get_category_icon(category_name: str) -> str:
    """Get icon for a category"""
    category = config.INDUSTRY_HIERARCHY.get(category_name)
    return category.get("icon", "🏢") if category else "🏢"

# ==================== RUN VALIDATION ====================
try:
    if validate_configuration():
        config_type = "Pydantic" if USE_PYDANTIC else "Simple"
        print("=" * 80)
        print(f"🌍 Global AI Powered Lead Generation System")
        print("=" * 80)
        print(f"✅ Configuration loaded ({config_type} mode)")
        print(f"📊 App: {config.APP_NAME} v{config.APP_VERSION}")
        print(f"🌐 Environment: {'Development' if config.DEBUG else 'Production'}")
        print(f"🗄️  Database: {config.DATABASE_NAME}")
        print(f"🌍 Countries: {len(config.COUNTRIES)}")
        print(f"🏢 Industries: {len(config.ALL_INDUSTRIES)}")
        print(f"📂 Categories: {len(config.INDUSTRY_HIERARCHY)}")
        print(f"🇪🇹 Ethiopian Market: {'Enabled' if config.ETHIOPIAN_MARKET_ENABLED else 'Disabled'}")
        print(f"🔗 CORS Origins: {config.CORS_ORIGINS}")
        print(f"🔌 API Integrations: {', '.join(config.API_INTEGRATIONS.keys())}")
        print("=" * 80)
    else:
        print("⚠️  Configuration has validation warnings but will continue")
except Exception as e:
    print(f"❌ Configuration validation failed: {e}")

# ==================== EXPORTS ====================
__all__ = [
    'config',
    'Settings',
    'SimpleConfig',
    'GLOBAL_CONFIG',
    'INDUSTRY_HIERARCHY',
    'ALL_INDUSTRIES',
    'ETHIOPIAN_CONFIG',
    'API_KEYS',
    'ICP_RULES',
    'SOURCES',
    'get_config_dict',
    'validate_configuration',
    'is_development',
    'is_production',
    'get_api_url',
    'get_database_url',
    'get_config_summary',
    'get_country_by_code',
    'get_country_name',
    'get_country_flag',
    'get_industries_by_category',
    'get_all_categories',
    'get_category_icon'
]

# ==================== TEST CONFIGURATION ====================
if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("CONFIGURATION TEST")
    print("=" * 80)
    
    print(f"\n📊 Application Settings:")
    print(f"  Name: {config.APP_NAME}")
    print(f"  Version: {config.APP_VERSION}")
    print(f"  Environment: {'Development' if config.DEBUG else 'Production'}")
    print(f"  Host: {config.HOST}:{config.PORT}")
    print(f"  API Prefix: {config.API_PREFIX}")
    
    print(f"\n🌍 Global Settings:")
    print(f"  Countries: {len(config.COUNTRIES)}")
    print(f"  First 5 Countries:")
    for country in config.COUNTRIES[:5]:
        print(f"    {country['flag']} {country['code']} - {country['name']}")
    
    print(f"\n🏢 Industry Settings:")
    print(f"  Categories: {len(config.INDUSTRY_HIERARCHY)}")
    print(f"  Total Industries: {len(config.ALL_INDUSTRIES)}")
    print(f"  First 5 Categories:")
    for category in list(config.INDUSTRY_HIERARCHY.keys())[:5]:
        icon = config.INDUSTRY_HIERARCHY[category]['icon']
        count = len(config.INDUSTRY_HIERARCHY[category]['industries'])
        print(f"    {icon} {category}: {count} industries")
    
    print(f"\n🇪🇹 Ethiopian Market:")
    print(f"  Enabled: {config.ETHIOPIAN_MARKET_ENABLED}")
    print(f"  Regions: {len(config.ETHIOPIAN_CONFIG['regions'])}")
    print(f"  Cities: {len(config.ETHIOPIAN_CONFIG['cities'])}")
    print(f"  Directories: {len(config.ETHIOPIAN_CONFIG['directories'])}")
    
    print(f"\n🔌 API Integrations:")
    for name, info in config.API_INTEGRATIONS.items():
        status = "✅" if info.get('enabled') else "❌"
        print(f"  {status} {name}")
    
    print(f"\n📋 ICP Rules:")
    print(f"  Target Industries: {len(config.ICP_RULES['industries'])}")
    print(f"  Employees: {config.ICP_RULES['min_employees']}-{config.ICP_RULES['max_employees']}")
    print(f"  Target Roles: {len(config.ICP_RULES['target_roles'])}")
    
    print(f"\n🗄️ Database:")
    print(f"  Name: {config.DATABASE_NAME}")
    print(f"  URI: {'[SET]' if config.MONGODB_URI else '[MISSING]'}")
    
    print(f"\n✅ Configuration test completed successfully!")
    print("=" * 80)