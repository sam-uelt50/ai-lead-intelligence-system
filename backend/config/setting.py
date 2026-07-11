# backend/config/settings.py
import os
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings - Centralized configuration"""
    
    # ==================== APPLICATION ====================
    APP_NAME: str = "Agency Lead Intelligence"
    APP_VERSION: str = "4.0.0"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # ==================== SERVER ====================
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8007"))
    
    # ==================== CORS ====================
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:5500,http://localhost:8007").split(",")
    ALLOWED_HOSTS: List[str] = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    
    # ==================== MONGODB ATLAS ====================
    MONGO_USER: str = os.getenv("MONGO_USER", "samueltesema56_db_user")
    MONGO_PASS: str = os.getenv("MONGO_PASS", "sam123")
    MONGO_HOST: str = os.getenv("MONGO_HOST", "cluster0.4dfoa3f.mongodb.net")
    MONGO_DB: str = os.getenv("MONGO_DB", "agency_intel")
    MONGO_PARAMS: str = os.getenv("MONGO_PARAMS", "?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true")
    
    @property
    def MONGODB_URI(self) -> str:
        """Build MongoDB URI with credentials"""
        import urllib.parse
        password = urllib.parse.quote_plus(self.MONGO_PASS)
        return f"mongodb+srv://{self.MONGO_USER}:{password}@{self.MONGO_HOST}/{self.MONGO_DB}{self.MONGO_PARAMS}"
    
    # ==================== 🔴 REAL API KEYS ====================
    
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
    
    # ==================== SECURITY ====================
    SECRET_KEY: str = os.getenv("SECRET_KEY", "test-token-2024")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ==================== RATE LIMITING ====================
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    # ==================== LOGGING ====================
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

# Create a single instance to import
settings = Settings()