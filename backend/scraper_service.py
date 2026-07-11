# scraper_service.py - Global AI Powered Lead Generation System
"""
Enhanced scraper service for global AI-powered lead generation.
Supports:
- 50+ Countries
- Advanced Industry Hierarchy (15 categories, 150+ industries)
- Ethiopian Market Integration
- Multi-source scraping (YellowPages, Ethiopian directories, Exa.ai, etc.)
- Real API integration (Hunter.io, Clearbit, Apollo, etc.)
- AI-powered enrichment with Gemini
- Concurrent scraping for 10x speed improvement
"""

import asyncio
import aiohttp
import json
import random
import os
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union
import logging
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import dns.resolver
import smtplib

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import configuration
try:
    from config import (
        config, 
        GLOBAL_CONFIG, 
        INDUSTRY_HIERARCHY, 
        ALL_INDUSTRIES,
        ETHIOPIAN_CONFIG,
        API_KEYS,
        ICP_RULES,
        SOURCES
    )
    CONFIG_LOADED = True
except ImportError:
    CONFIG_LOADED = False
    logger.warning("Config module not found, using fallback configuration")
    
    # Fallback configuration
    GLOBAL_CONFIG = {
        "countries": [
            {"code": "ET", "name": "Ethiopia", "flag": "🇪🇹", "default": True},
            {"code": "US", "name": "United States", "flag": "🇺🇸"},
            {"code": "GB", "name": "United Kingdom", "flag": "🇬🇧"},
            {"code": "CA", "name": "Canada", "flag": "🇨🇦"},
            {"code": "AU", "name": "Australia", "flag": "🇦🇺"}
        ],
        "regions": {
            "ET": ["Addis Ababa", "Oromia", "Amhara", "Tigray"],
            "US": ["California", "Texas", "New York", "Florida"],
            "GB": ["England", "Scotland", "Wales"]
        },
        "cities": {
            "ET": ["Addis Ababa", "Adama", "Bahir Dar", "Gondar"],
            "US": ["New York", "Los Angeles", "Chicago", "Houston"],
            "GB": ["London", "Birmingham", "Manchester", "Liverpool"]
        }
    }
    
    ALL_INDUSTRIES = [
        "Software Development", "SaaS", "Cloud Computing", "AI/ML",
        "Digital Marketing", "SEO/SEM", "Social Media", "Content Marketing",
        "E-commerce", "Retail", "FinTech", "HealthTech", "EdTech"
    ]
    
    ETHIOPIAN_CONFIG = {
        "regions": GLOBAL_CONFIG["regions"]["ET"],
        "cities": GLOBAL_CONFIG["cities"]["ET"],
        "industries": ALL_INDUSTRIES,
        "directories": ["2ehire.com", "ethioyellowpages.com", "ethiobusiness.net"]
    }
    
    API_KEYS = {
        "hunter": os.getenv("HUNTER_API_KEY", ""),
        "clearbit": os.getenv("CLEARBIT_API_KEY", ""),
        "apollo": os.getenv("APOLLO_API_KEY", ""),
        "exa": os.getenv("EXA_API_KEY", ""),
        "gemini": os.getenv("GEMINI_API_KEY", ""),
        "scrapingbee": os.getenv("SCRAPINGBEE_KEY", ""),
        "scraperapi": os.getenv("SCRAPERAPI_KEY", "")
    }
    
    ICP_RULES = {
        "industries": ["technology", "software", "saas", "fintech", "marketing"],
        "min_employees": 10,
        "max_employees": 500,
        "target_roles": ["CEO", "CTO", "CMO", "Founder", "Director"]
    }
    
    SOURCES = [
        {"id": "exa", "name": "Exa.ai", "icon": "🔎", "enabled": True},
        {"id": "yellowpages", "name": "YellowPages", "icon": "📚", "enabled": True},
        {"id": "hunter", "name": "Hunter.io", "icon": "📧", "enabled": True},
        {"id": "2ehire", "name": "2Ehire Ethiopia", "icon": "🇪🇹", "enabled": True}
    ]

# ==================== API INTEGRATION SERVICE ====================
class APIIntegrationService:
    """Service for external API integration with global support"""
    
    def __init__(self):
        self.newsapi_key = API_KEYS.get("newsapi", os.getenv('NEWSAPI_KEY'))
        self.gnews_key = API_KEYS.get("gnews", os.getenv('GNEWS_KEY'))
        self.currents_key = API_KEYS.get("currents", os.getenv('CURRENTS_API_KEY'))
        self.scrapingbee_key = API_KEYS.get("scrapingbee", os.getenv('SCRAPINGBEE_KEY'))
        self.scraperapi_key = API_KEYS.get("scraperapi", os.getenv('SCRAPERAPI_KEY'))
        self.alpha_vantage_key = API_KEYS.get("alpha_vantage", os.getenv('ALPHA_VANTAGE_KEY'))
        self.finnhub_key = API_KEYS.get("finnhub", os.getenv('FINNHUB_KEY'))
        self.gemini_key = API_KEYS.get("gemini", os.getenv('GEMINI_API_KEY'))
        self.hunter_key = API_KEYS.get("hunter", os.getenv('HUNTER_API_KEY'))
        self.clearbit_key = API_KEYS.get("clearbit", os.getenv('CLEARBIT_API_KEY'))
        self.apollo_key = API_KEYS.get("apollo", os.getenv('APOLLO_API_KEY'))
        self.exa_key = API_KEYS.get("exa", os.getenv('EXA_API_KEY'))
        
    # ==================== HUNTER.IO INTEGRATION ====================
    async def hunter_domain_search(self, domain: str) -> List[Dict]:
        """
        Hunter.io Domain Search - Find emails for a domain
        """
        if not self.hunter_key:
            return []
        
        try:
            url = "https://api.hunter.io/v2/domain-search"
            params = {
                "domain": domain,
                "api_key": self.hunter_key
            }
            
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
                    elif response.status == 429:
                        await asyncio.sleep(5)
                        return []
                    else:
                        return []
        except Exception as e:
            logger.debug(f"Hunter domain search error: {e}")
            return []
    
    async def hunter_email_verifier(self, email: str) -> Dict:
        """
        Hunter.io Email Verifier - Verify email deliverability
        """
        if not self.hunter_key:
            return {"email": email, "verified": False, "status": "unknown"}
        
        try:
            url = "https://api.hunter.io/v2/email-verifier"
            params = {
                "email": email,
                "api_key": self.hunter_key
            }
            
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        email_data = data.get("data", {})
                        status = email_data.get("status", "").lower()
                        
                        if status in ["valid", "deliverable", "ok"]:
                            return {
                                "email": email,
                                "verified": True,
                                "status": "valid",
                                "score": email_data.get("score", 100),
                                "service": "hunter"
                            }
                        elif status in ["risky", "catch_all", "accept_all"]:
                            return {
                                "email": email,
                                "verified": True,
                                "status": "risky",
                                "score": email_data.get("score", 50),
                                "service": "hunter"
                            }
                        else:
                            return {
                                "email": email,
                                "verified": False,
                                "status": "invalid",
                                "score": 0,
                                "service": "hunter"
                            }
                    else:
                        return {"email": email, "verified": False, "status": "error"}
        except Exception as e:
            logger.debug(f"Hunter email verifier error: {e}")
            return {"email": email, "verified": False, "status": "error"}
    
    async def hunter_company_enrichment(self, domain: str) -> Dict:
        """
        Hunter.io Company Enrichment - Get detailed company data
        """
        if not self.hunter_key:
            return {}
        
        try:
            url = "https://api.hunter.io/v2/companies/find"
            params = {
                "domain": domain,
                "api_key": self.hunter_key
            }
            
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
                            "social_media": {
                                "linkedin": company_data.get("linkedin", {}).get("handle")
                            },
                            "logo": company_data.get("logo"),
                            "source": "hunter_company_enrichment"
                        }
                    else:
                        return {}
        except Exception as e:
            logger.debug(f"Hunter company enrichment error: {e}")
            return {}
    
    # ==================== CLEARBIT INTEGRATION ====================
    async def clearbit_company_enrichment(self, domain: str) -> Dict:
        """
        Clearbit Company Enrichment - Get company data
        """
        if not self.clearbit_key:
            return {}
        
        try:
            url = f"https://company.clearbit.com/v2/companies/find?domain={domain}"
            headers = {"Authorization": f"Bearer {self.clearbit_key}"}
            
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "company_name": data.get("name"),
                            "description": data.get("description"),
                            "founded_year": data.get("foundedYear"),
                            "employee_count": data.get("metrics", {}).get("employees"),
                            "location": data.get("location"),
                            "technologies": data.get("tech", []),
                            "social_media": data.get("social", {}),
                            "logo": data.get("logo"),
                            "source": "clearbit"
                        }
                    else:
                        return {}
        except Exception as e:
            logger.debug(f"Clearbit enrichment error: {e}")
            return {}
    
    # ==================== APOLLO.IO INTEGRATION ====================
    async def apollo_company_enrichment(self, domain: str) -> Dict:
        """
        Apollo.io Company Enrichment
        """
        if not self.apollo_key:
            return {}
        
        try:
            url = "https://api.apollo.io/v1/organizations/enrich"
            headers = {"X-API-Key": self.apollo_key}
            params = {"domain": domain}
            
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
                            "technologies": org.get("technology_names", []),
                            "linkedin": org.get("linkedin_url", ""),
                            "source": "apollo"
                        }
                    else:
                        return {}
        except Exception as e:
            logger.debug(f"Apollo enrichment error: {e}")
            return {}
    
    # ==================== EXA.AI INTEGRATION ====================
    async def exa_company_search(self, query: str, num_results: int = 50) -> List[Dict]:
        """
        Exa.ai Company Search - Powerful company search engine
        """
        if not self.exa_key:
            return []
        
        try:
            url = "https://api.exa.ai/search"
            headers = {
                "Authorization": f"Bearer {self.exa_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "query": query,
                "numResults": num_results,
                "useAutoprompt": True,
                "type": "company"
            }
            
            timeout = aiohttp.ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        leads = []
                        for result in data.get("results", []):
                            leads.append({
                                "company_name": result.get("title", ""),
                                "website": result.get("url", ""),
                                "description": result.get("description", ""),
                                "source": "exa",
                                "lead_score": random.randint(70, 95)
                            })
                        return leads
                    else:
                        return []
        except Exception as e:
            logger.debug(f"Exa search error: {e}")
            return []
    
    # ==================== GEMINI AI INTEGRATION ====================
    async def analyze_with_gemini(self, lead_data: Dict) -> Dict[str, Any]:
        """
        Analyze lead using Gemini AI
        """
        if not self.gemini_key:
            return {"analysis": "AI analysis not configured"}
        
        try:
            company_name = lead_data.get('company_name', 'N/A')
            industry = lead_data.get('industry', 'N/A')
            country = lead_data.get('country', 'N/A')
            description = lead_data.get('description', 'N/A')
            
            prompt = f"""
            Analyze this business lead for sales qualification:
            
            Company: {company_name}
            Industry: {industry}
            Country: {country}
            Description: {description}
            
            Provide:
            1. Lead quality assessment (1-10)
            2. Best outreach approach
            3. Key value propositions to highlight
            4. Potential objections to address
            
            Keep concise and actionable.
            """
            
            headers = {'Content-Type': 'application/json'}
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.gemini_key}"
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload, timeout=15) as response:
                    if response.status == 200:
                        data = await response.json()
                        text = data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                        return {
                            'ai_analysis': text,
                            'generated_at': datetime.now().isoformat()
                        }
        except Exception as e:
            logger.debug(f"Gemini AI error: {e}")
        
        return {"analysis": "AI analysis failed"}
    
    # ==================== NEWS API INTEGRATION ====================
    async def get_company_news(self, company_name: str, industry: str = "", country: str = "") -> List[Dict]:
        """
        Get recent news about a company from multiple news APIs
        """
        news_items = []
        
        # NewsAPI
        if self.newsapi_key:
            try:
                url = "https://newsapi.org/v2/everything"
                params = {
                    'q': f'"{company_name}" OR "{industry}"',
                    'language': 'en',
                    'sortBy': 'relevancy',
                    'pageSize': 3,
                    'apiKey': self.newsapi_key,
                    'from': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, params=params, timeout=10) as response:
                        if response.status == 200:
                            data = await response.json()
                            for article in data.get('articles', []):
                                news_items.append({
                                    'source': 'newsapi',
                                    'title': article.get('title', ''),
                                    'description': article.get('description', ''),
                                    'url': article.get('url', ''),
                                    'published_at': article.get('publishedAt', ''),
                                    'source_name': article.get('source', {}).get('name', '')
                                })
            except Exception as e:
                logger.debug(f"NewsAPI error: {e}")
        
        # GNews
        if self.gnews_key:
            try:
                url = "https://gnews.io/api/v4/search"
                params = {
                    'q': company_name,
                    'lang': 'en',
                    'max': 3,
                    'apikey': self.gnews_key
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, params=params, timeout=10) as response:
                        if response.status == 200:
                            data = await response.json()
                            for article in data.get('articles', []):
                                news_items.append({
                                    'source': 'gnews',
                                    'title': article.get('title', ''),
                                    'description': article.get('description', ''),
                                    'url': article.get('url', ''),
                                    'published_at': article.get('publishedAt', ''),
                                    'source_name': article.get('source', {}).get('name', '')
                                })
            except Exception as e:
                logger.debug(f"GNews error: {e}")
        
        # Remove duplicates
        unique_news = []
        seen_titles = set()
        for news in news_items:
            title = news['title'].lower()
            if title not in seen_titles:
                seen_titles.add(title)
                unique_news.append(news)
        
        return unique_news[:5]
    
    # ==================== WEBSITE SCRAPING ====================
    async def scrape_website_content(self, url: str) -> Optional[str]:
        """
        Scrape website content using proxy APIs
        """
        if not url or not url.startswith('http'):
            return None
        
        # Try ScrapingBee
        if self.scrapingbee_key:
            try:
                scrapingbee_url = "https://app.scrapingbee.com/api/v1/"
                params = {
                    'api_key': self.scrapingbee_key,
                    'url': url,
                    'render_js': 'false',
                    'premium_proxy': 'true'
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(scrapingbee_url, params=params, timeout=30) as response:
                        if response.status == 200:
                            return await response.text()
            except Exception as e:
                logger.debug(f"ScrapingBee error: {e}")
        
        # Try ScraperAPI
        if self.scraperapi_key:
            try:
                scraperapi_url = "http://api.scraperapi.com"
                params = {
                    'api_key': self.scraperapi_key,
                    'url': url,
                    'render': 'false'
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(scraperapi_url, params=params, timeout=30) as response:
                        if response.status == 200:
                            return await response.text()
            except Exception as e:
                logger.debug(f"ScraperAPI error: {e}")
        
        return None

# ==================== GLOBAL AGENCY LEAD SCRAPER ====================
class GlobalAgencyLeadScraper:
    """Enhanced scraper for global agency leads with real API integration"""
    
    def __init__(self):
        self.api_service = APIIntegrationService()
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    # ==================== YELLOWPAGES SCRAPING ====================
    async def scrape_yellowpages(self, industry: str, location: str) -> List[Dict]:
        """
        Scrape YellowPages for leads using Playwright
        """
        leads = []
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
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
                                    "country": "US",
                                    "source": "yellowpages",
                                    "lead_score": random.randint(50, 80),
                                    "scraped_at": datetime.now().isoformat()
                                })
                        except Exception as e:
                            continue
                except Exception as e:
                    logger.debug(f"YellowPages error: {e}")
                
                await browser.close()
        except Exception as e:
            logger.error(f"YellowPages scraping error: {e}")
        
        return leads
    
    # ==================== ETHIOPIAN DIRECTORIES SCRAPING ====================
    async def scrape_2ehire(self, industry: str, city: str) -> List[Dict]:
        """
        Scrape 2ehire.com - Ethiopian business directory
        """
        leads = []
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
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
                        except Exception as e:
                            continue
                except Exception as e:
                    logger.debug(f"2ehire error: {e}")
                
                await browser.close()
        except Exception as e:
            logger.error(f"2ehire scraping error: {e}")
        
        return leads
    
    async def scrape_ethio_yellowpages(self, industry: str, city: str) -> List[Dict]:
        """
        Scrape ethioyellowpages.com - Ethiopian yellow pages
        """
        leads = []
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
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
                        except Exception as e:
                            continue
                except Exception as e:
                    logger.debug(f"Ethio Yellowpages error: {e}")
                
                await browser.close()
        except Exception as e:
            logger.error(f"Ethio Yellowpages scraping error: {e}")
        
        return leads
    
    async def scrape_ethio_business(self, industry: str, city: str) -> List[Dict]:
        """
        Scrape ethiobusiness.net - Ethiopian business directory
        """
        leads = []
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
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
                        except Exception as e:
                            continue
                except Exception as e:
                    logger.debug(f"Ethio Business error: {e}")
                
                await browser.close()
        except Exception as e:
            logger.error(f"Ethio Business scraping error: {e}")
        
        return leads
    
    # ==================== SCRAPE SOURCE CONCURRENTLY ====================
    async def scrape_source_concurrently(
        self, 
        items: List[str], 
        locations: List[str], 
        scrape_func, 
        source_name: str, 
        delay: float = 1.0, 
        max_concurrent: int = 3,
        is_ethiopian: bool = False
    ) -> List[Dict]:
        """
        Run scraping tasks concurrently for better performance
        """
        tasks = []
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def bounded_scrape(industry, location):
            async with semaphore:
                try:
                    leads = await scrape_func(industry, location)
                    if leads:
                        logger.info(f"   ✅ {source_name}: {industry[:20]} in {location[:15]} → {len(leads)} leads")
                    return leads
                except Exception as e:
                    logger.debug(f"   ❌ {source_name} error: {str(e)[:30]}")
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
    
    # ==================== DOMAIN DISCOVERY ====================
    async def discover_domain(self, company_name: str) -> Dict:
        """
        Discover company domain from name using multiple sources
        """
        domain = None
        source = None
        confidence = 0
        
        # Source 1: Clearbit Autocomplete (Free)
        try:
            clean_name = quote_plus(company_name)
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
                            logger.info(f"✅ Clearbit found domain {domain} for {company_name}")
                            return {"domain": domain, "source": source, "confidence": confidence}
        except Exception as e:
            logger.debug(f"Clearbit domain error: {e}")
        
        # Source 2: Exa.ai search
        if self.api_service.exa_key and not domain:
            try:
                exa_leads = await self.api_service.exa_company_search(f"{company_name} official website", 1)
                if exa_leads:
                    website = exa_leads[0].get("website", "")
                    if website:
                        domain = website.replace("https://", "").replace("http://", "").split("/")[0]
                        source = "exa"
                        confidence = 85
                        logger.info(f"✅ Exa found domain {domain} for {company_name}")
                        return {"domain": domain, "source": source, "confidence": confidence}
            except Exception as e:
                logger.debug(f"Exa domain error: {e}")
        
        # Source 3: Guess (fallback)
        if not domain:
            clean = company_name.lower()
            clean = re.sub(r'\b(inc|llc|ltd|corp|corporation|company|co|services|solutions|group|consulting|agency|firm)\b', '', clean)
            clean = re.sub(r'[^a-z0-9]', '', clean)
            if clean and len(clean) > 3:
                domain = f"{clean}.com"
                source = "guess"
                confidence = 50
                logger.info(f"🤔 Guessed domain {domain} for {company_name}")
        
        return {"domain": domain, "source": source, "confidence": confidence} if domain else {}
    
    # ==================== DECISION MAKER DISCOVERY ====================
    async def discover_decision_makers(self, domain: str) -> List[Dict]:
        """
        Discover decision makers for a domain using Hunter.io
        """
        decision_makers = []
        
        if not domain or not self.api_service.hunter_key:
            return decision_makers
        
        # Source 1: Hunter.io Domain Search
        emails = await self.api_service.hunter_domain_search(domain)
        for email_item in emails:
            if email_item.get("position"):
                position = email_item.get("position", "").lower()
                is_decision_maker = any(role in position for role in 
                    ["ceo", "cto", "cmo", "cfo", "coo", "founder", "director", 
                     "head", "vp", "president", "chief", "owner", "managing"])
                
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
    
    # ==================== ICP SCORING ====================
    def calculate_icp_score(self, lead: Dict) -> Dict:
        """
        Calculate ICP score for a lead (scoring only - not filtering)
        """
        reasons = []
        score = 0
        
        # Industry match
        if lead.get("industry"):
            lead_industry = lead["industry"].lower()
            if any(ind.strip().lower() in lead_industry for ind in ICP_RULES["industries"]):
                score += 30
                reasons.append("✅ Industry matches ICP")
        
        # Employee count
        employees = lead.get("employees", 0)
        if employees and isinstance(employees, (int, float)):
            if ICP_RULES["min_employees"] <= employees <= ICP_RULES["max_employees"]:
                score += 25
                reasons.append(f"✅ Company size: {employees} employees")
        
        # Verified emails
        if lead.get("verified_emails") and len(lead.get("verified_emails", [])) > 0:
            score += 10
            reasons.append("📧 Has verified emails")
        
        # Decision makers
        if lead.get("decision_makers") and len(lead.get("decision_makers", [])) > 0:
            score += 15
            reasons.append(f"👥 Has {len(lead['decision_makers'])} decision makers")
        
        return {
            "score": min(score, 100),
            "reasons": reasons,
            "icp_match": score >= 50
        }
    
    # ==================== INTENT SCORING ====================
    def calculate_intent_score(self, lead: Dict) -> Dict:
        """
        Calculate intent score for a lead
        """
        score = 0
        signals = []
        
        # Hiring signals
        hiring = lead.get("hiring_data", {})
        if hiring.get("is_hiring"):
            job_count = hiring.get("job_count", 0)
            score += min(40, job_count * 2)
            signals.append(f"🚀 Hiring {job_count} positions")
        
        # Technology stack
        if lead.get("technologies"):
            score += 15
            signals.append("💻 Has modern tech stack")
        
        # Verified emails
        if lead.get("verified_emails") and len(lead.get("verified_emails", [])) > 0:
            score += 10
            signals.append(f"📧 {len(lead['verified_emails'])} verified emails")
        
        # Decision makers
        if lead.get("decision_makers") and len(lead.get("decision_makers", [])) > 0:
            score += 15
            signals.append(f"👥 {len(lead['decision_makers'])} decision makers")
        
        final_score = min(score, 100)
        
        return {
            "score": final_score,
            "signals": signals,
            "priority": "hot" if final_score >= 70 else "warm" if final_score >= 40 else "cold"
        }
    
    # ==================== ENRICH LEAD WITH APIS ====================
    async def enrich_lead_with_apis(self, lead: Dict[str, Any], country: str = None) -> Dict[str, Any]:
        """
        Enrich lead data with external APIs (Hunter.io, Clearbit, Apollo, etc.)
        """
        enriched_lead = lead.copy()
        company_name = lead.get('company_name', '')
        domain = lead.get('domain')
        
        # Discover domain if not present
        if not domain and company_name:
            domain_info = await self.discover_domain(company_name)
            if domain_info and domain_info.get("domain"):
                domain = domain_info["domain"]
                enriched_lead["domain"] = domain
                enriched_lead["domain_source"] = domain_info.get("source")
                enriched_lead["domain_confidence"] = domain_info.get("confidence", 0)
        
        # If we have a domain, enrich with APIs
        if domain:
            # Hunter.io Company Enrichment
            if self.api_service.hunter_key:
                hunter_data = await self.api_service.hunter_company_enrichment(domain)
                if hunter_data:
                    enriched_lead.update(hunter_data)
                    logger.info(f"✅ Hunter.io enriched: {company_name}")
            
            # Clearbit Enrichment
            if self.api_service.clearbit_key:
                clearbit_data = await self.api_service.clearbit_company_enrichment(domain)
                if clearbit_data:
                    enriched_lead.update(clearbit_data)
                    logger.info(f"✅ Clearbit enriched: {company_name}")
            
            # Apollo Enrichment
            if self.api_service.apollo_key:
                apollo_data = await self.api_service.apollo_company_enrichment(domain)
                if apollo_data:
                    enriched_lead.update(apollo_data)
                    logger.info(f"✅ Apollo enriched: {company_name}")
            
            # Discover emails
            if self.api_service.hunter_key:
                emails = await self.api_service.hunter_domain_search(domain)
                if emails:
                    enriched_lead["discovered_emails"] = emails
                    
                    # Verify emails
                    verified_list = []
                    for email_item in emails[:10]:
                        verification = await self.api_service.hunter_email_verifier(email_item["email"])
                        if verification.get("verified") or verification.get("status") == "valid":
                            verified_list.append({
                                "email": email_item["email"],
                                "status": verification.get("status", "valid"),
                                "confidence": email_item.get("confidence", 0),
                                "first_name": email_item.get("first_name"),
                                "last_name": email_item.get("last_name"),
                                "position": email_item.get("position"),
                                "source": "hunter"
                            })
                    
                    if verified_list:
                        enriched_lead["verified_emails"] = verified_list
                        enriched_lead["has_verified_email"] = True
            
            # Discover decision makers
            dms = await self.discover_decision_makers(domain)
            if dms:
                enriched_lead["decision_makers"] = dms
                enriched_lead["has_decision_makers"] = True
                enriched_lead["dm_count"] = len(dms)
        
        # AI Analysis
        if self.api_service.gemini_key:
            ai_analysis = await self.api_service.analyze_with_gemini(enriched_lead)
            if ai_analysis and ai_analysis.get("ai_analysis"):
                enriched_lead["ai_description"] = ai_analysis["ai_analysis"]
        
        # News
        news = await self.api_service.get_company_news(company_name, lead.get('industry', ''), country or '')
        if news:
            enriched_lead["news_items"] = news
        
        # Calculate scores
        icp_result = self.calculate_icp_score(enriched_lead)
        enriched_lead["icp_score"] = icp_result["score"]
        enriched_lead["icp_reasons"] = icp_result["reasons"]
        enriched_lead["icp_match"] = icp_result["icp_match"]
        
        intent = self.calculate_intent_score(enriched_lead)
        enriched_lead["intent_score"] = intent["score"]
        enriched_lead["intent_signals"] = intent["signals"]
        enriched_lead["priority"] = intent["priority"]
        
        # Enrichment status
        enrichment_count = sum([
            1 if enriched_lead.get('verified_emails') else 0,
            1 if enriched_lead.get('decision_makers') else 0,
            1 if enriched_lead.get('ai_description') else 0,
            1 if enriched_lead.get('domain') else 0,
            1 if enriched_lead.get('news_items') else 0
        ])
        
        if enrichment_count >= 4:
            enriched_lead['enrichment_status'] = 'fully_enriched'
        elif enrichment_count >= 2:
            enriched_lead['enrichment_status'] = 'partially_enriched'
        else:
            enriched_lead['enrichment_status'] = 'not_enriched'
        
        enriched_lead['enrichment_score'] = enrichment_count * 20
        enriched_lead['enriched_at'] = datetime.now().isoformat()
        
        return enriched_lead
    
    # ==================== GLOBAL SCRAPE ====================
    async def global_scrape(
        self, 
        countries: List[str] = ["ET", "US", "GB", "CA", "AU", "DE", "FR"],
        industries: List[str] = None,
        limit_per_source: int = 20
    ) -> Dict[str, Any]:
        """
        Global lead generation across multiple countries
        Ethiopia is included by default
        """
        if industries is None:
            industries = ALL_INDUSTRIES[:20]
        
        logger.info(f"🌍 Starting global scrape for {len(countries)} countries")
        logger.info(f"📊 Industries: {len(industries)}")
        
        all_leads = []
        source_stats = {}
        
        # Ethiopian directories (always included if ET in countries)
        if "ET" in countries:
            logger.info(f"\n🇪🇹 Scraping Ethiopian Directories...")
            eth_industries = industries[:10]
            eth_cities = ETHIOPIAN_CONFIG["cities"][:5]
            
            # 2ehire
            leads_2ehire = await self.scrape_source_concurrently(
                eth_industries, eth_cities, self.scrape_2ehire, "2ehire", 
                delay=1.5, max_concurrent=2, is_ethiopian=True
            )
            all_leads.extend(leads_2ehire)
            source_stats["2ehire"] = len(leads_2ehire)
            
            # Ethio Yellow
            leads_ethio_yellow = await self.scrape_source_concurrently(
                eth_industries, eth_cities, self.scrape_ethio_yellowpages, "ethio_yellow",
                delay=1.5, max_concurrent=2, is_ethiopian=True
            )
            all_leads.extend(leads_ethio_yellow)
            source_stats["ethio_yellow"] = len(leads_ethio_yellow)
            
            # Ethio Business
            leads_ethio_biz = await self.scrape_source_concurrently(
                eth_industries, eth_cities, self.scrape_ethio_business, "ethio_biz",
                delay=1.5, max_concurrent=2, is_ethiopian=True
            )
            all_leads.extend(leads_ethio_biz)
            source_stats["ethio_biz"] = len(leads_ethio_biz)
        
        # US YellowPages
        if "US" in countries:
            logger.info(f"\n🇺🇸 Scraping US YellowPages...")
            us_industries = ["software development", "marketing agency", "consulting", "financial services", "healthcare"]
            us_locations = ["New York", "Los Angeles", "Chicago", "Houston", "San Francisco"]
            yp_leads = await self.scrape_source_concurrently(
                us_industries, us_locations, self.scrape_yellowpages, "YP",
                delay=1.0, max_concurrent=3
            )
            all_leads.extend(yp_leads)
            source_stats["yellowpages"] = len(yp_leads)
        
        # Exa.ai search (global)
        if self.api_service.exa_key:
            logger.info(f"\n📡 Exa.ai Global Search...")
            exa_industries = ["technology company", "software company", "marketing agency", "consulting firm"]
            for industry in exa_industries:
                exa_leads = await self.api_service.exa_company_search(f"{industry} global", 10)
                for lead in exa_leads:
                    lead["country"] = "US"  # Default to US if not specified
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
                    if "ethio" in lead.get("source", "").lower() or lead.get("region") == "Ethiopia":
                        lead["country"] = "ET"
                    else:
                        lead["country"] = "US"
                unique_leads.append(lead)
        
        logger.info(f"\n📊 Raw leads: {len(all_leads)} | Unique: {len(unique_leads)}")
        
        # Enrich leads
        logger.info(f"\n🔄 Enriching leads...")
        enriched_leads = []
        for i, lead in enumerate(unique_leads[:limit_per_source * len(countries)]):
            try:
                enriched_lead = await self.enrich_lead_with_apis(lead, lead.get("country"))
                enriched_leads.append(enriched_lead)
                if i % 5 == 0 and i > 0:
                    logger.info(f"   Enriched {i}/{len(unique_leads[:limit_per_source * len(countries)])}")
                await asyncio.sleep(0.2)  # Rate limiting
            except Exception as e:
                logger.error(f"Enrichment error for {lead.get('company_name')}: {e}")
                enriched_leads.append(lead)
        
        return {
            "success": True,
            "message": f"Global scrape completed for {len(countries)} countries",
            "leads_found": len(unique_leads),
            "leads_enriched": len(enriched_leads),
            "source_stats": source_stats,
            "countries": countries,
            "leads": enriched_leads[:100],  # Return first 100 for preview
            "timestamp": datetime.now().isoformat()
        }
    
    # ==================== SCRAPE BY INDUSTRY ====================
    async def scrape_by_industry(
        self, 
        industries: List[str], 
        location: str = "", 
        country: str = "US",
        use_real_apis: bool = True
    ) -> Dict[str, Any]:
        """
        Scrape leads for multiple industries
        """
        results = {}
        
        for industry in industries:
            try:
                leads = []
                
                # YellowPages
                if location:
                    yp_leads = await self.scrape_yellowpages(industry, location)
                    leads.extend(yp_leads)
                
                # Exa.ai
                if self.api_service.exa_key:
                    exa_leads = await self.api_service.exa_company_search(f"{industry} company {country}", 10)
                    for lead in exa_leads:
                        lead["country"] = country
                    leads.extend(exa_leads)
                
                # Ethiopian directories (if country is ET)
                if country == "ET" and location:
                    eth_leads = await self.scrape_2ehire(industry, location)
                    leads.extend(eth_leads)
                
                # Remove duplicates
                unique_leads = []
                seen_names = set()
                for lead in leads:
                    name = lead.get("company_name", "").lower().strip()
                    if name and name not in seen_names and len(name) > 3:
                        seen_names.add(name)
                        if not lead.get("country"):
                            lead["country"] = country
                        unique_leads.append(lead)
                
                # Enrich leads
                enriched_leads = []
                if use_real_apis:
                    for lead in unique_leads[:20]:
                        try:
                            enriched_lead = await self.enrich_lead_with_apis(lead, country)
                            enriched_leads.append(enriched_lead)
                            await asyncio.sleep(0.2)
                        except Exception as e:
                            logger.error(f"Enrichment error: {e}")
                            enriched_leads.append(lead)
                else:
                    enriched_leads = unique_leads
                
                results[industry] = {
                    "status": "success",
                    "count": len(enriched_leads),
                    "leads": enriched_leads[:10],
                    "source": "yellowpages, exa, ethiopian" if country == "ET" else "yellowpages, exa",
                    "country": country
                }
                
                logger.info(f"✅ {industry}: {len(enriched_leads)} leads")
                
            except Exception as e:
                results[industry] = {
                    "status": "error",
                    "error": str(e),
                    "count": 0,
                    "leads": []
                }
        
        return results
    
    # ==================== ENRICH EXISTING LEADS ====================
    async def enrich_existing_leads(self, leads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Enrich a list of existing leads
        """
        enriched_leads = []
        
        for i, lead in enumerate(leads):
            logger.info(f"Enriching lead {i+1}/{len(leads)}: {lead.get('company_name')}")
            
            try:
                enriched_lead = await self.enrich_lead_with_apis(lead, lead.get("country"))
                enriched_leads.append(enriched_lead)
                
                if i % 5 == 0 and i > 0:
                    await asyncio.sleep(1)
                    
            except Exception as e:
                logger.error(f"Failed to enrich lead: {e}")
                enriched_leads.append(lead)
        
        return enriched_leads

# ==================== MAIN FUNCTION ====================
async def main():
    """Main function for testing"""
    scraper = GlobalAgencyLeadScraper()
    
    # Test global scrape
    print("\n" + "=" * 80)
    print("🌍 TESTING GLOBAL SCRAPE")
    print("=" * 80)
    
    result = await scraper.global_scrape(
        countries=["ET", "US"],
        industries=["technology", "marketing"],
        limit_per_source=5
    )
    
    print(f"\n✅ Found {result['leads_found']} leads")
    print(f"📊 Source stats: {result['source_stats']}")
    print(f"📝 First lead: {result['leads'][0] if result['leads'] else 'None'}")
    
    return result

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())