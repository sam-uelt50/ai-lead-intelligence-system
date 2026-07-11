# backend/services/signal_detector.py
import aiohttp
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import re
import json

from config import config
from database.models.signal import SignalType

class SignalDetector:
    """Detect growth signals from various sources"""
    
    def __init__(self):
        self.session = None
        self.headers = {
            "User-Agent": "AgencyLeadIntelligence/1.0"
        }
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def detect_all_signals(self, company: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect all possible growth signals for a company"""
        signals = []
        
        tasks = [
            self.detect_hiring_signals(company),
            self.detect_funding_signals(company),
            self.detect_tech_signals(company),
            self.detect_expansion_signals(company),
            self.detect_news_signals(company)
        ]
        
        # Run all detectors in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Collect valid results
        for result in results:
            if isinstance(result, Exception):
                print(f"Signal detection error: {result}")
            elif result:
                signals.extend(result)
        
        return signals
    
    async def detect_hiring_signals(self, company: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect hiring/marketing job postings"""
        signals = []
        company_name = company.get("name", "")
        
        # Check LinkedIn (mock for now - you'd use LinkedIn API)
        linkedin_signals = await self._check_linkedin_jobs(company_name)
        signals.extend(linkedin_signals)
        
        # Check company career page
        website = company.get("website")
        if website:
            career_signals = await self._check_career_page(website)
            signals.extend(career_signals)
        
        return signals
    
    async def detect_funding_signals(self, company: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect recent funding rounds"""
        signals = []
        company_name = company.get("name", "")
        
        # Mock funding detection (in production, use Crunchbase API, PitchBook, etc.)
        mock_funding_data = self._get_mock_funding_data(company_name)
        
        if mock_funding_data:
            signals.append({
                "type": SignalType.FUNDING.value,
                "description": mock_funding_data["description"],
                "confidence": mock_funding_data["confidence"],
                "source": "Mock Funding Database",
                "detected_at": datetime.now(),
                "metadata": {
                    "amount": mock_funding_data.get("amount"),
                    "round": mock_funding_data.get("round"),
                    "date": mock_funding_data.get("date")
                }
            })
        
        return signals
    
    async def detect_tech_signals(self, company: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect technology stack changes"""
        signals = []
        website = company.get("website")
        
        if website:
            try:
                async with self.session.get(website, timeout=10) as response:
                    if response.status == 200:
                        html = await response.text()
                        
                        # Analyze tech stack
                        tech_findings = self._analyze_tech_stack(html)
                        
                        if tech_findings:
                            signals.append({
                                "type": SignalType.TECH_REFRESH.value,
                                "description": f"Tech stack detected: {', '.join(tech_findings)}",
                                "confidence": 70,
                                "source": "Website Analysis",
                                "detected_at": datetime.now(),
                                "metadata": {"technologies": tech_findings}
                            })
            except Exception as e:
                print(f"Tech signal detection failed for {website}: {e}")
        
        return signals
    
    async def detect_expansion_signals(self, company: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect expansion/news signals"""
        signals = []
        company_name = company.get("name", "")
        
        # Mock news detection
        mock_news = self._get_mock_company_news(company_name)
        
        for news_item in mock_news:
            signals.append({
                "type": SignalType.EXPANSION.value,
                "description": news_item["title"],
                "confidence": news_item["confidence"],
                "source": news_item["source"],
                "detected_at": datetime.now() - timedelta(days=news_item["days_ago"]),
                "metadata": {
                    "url": news_item.get("url"),
                    "category": news_item.get("category")
                }
            })
        
        return signals
    
    async def detect_news_signals(self, company: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect general news signals"""
        # In production, integrate with NewsAPI, Google News, etc.
        return []
    
    # Helper methods
    async def _check_linkedin_jobs(self, company_name: str) -> List[Dict[str, Any]]:
        """Check LinkedIn for job postings (mock implementation)"""
        # Mock data for demonstration
        mock_jobs = {
            "TechScale Inc": [
                {"title": "Director of Marketing", "days_ago": 5},
                {"title": "Growth Marketing Manager", "days_ago": 10}
            ],
            "GrowthLab SaaS": [
                {"title": "VP Marketing", "days_ago": 3},
                {"title": "Content Strategist", "days_ago": 7}
            ],
            "StartupXYZ": [
                {"title": "Marketing Lead", "days_ago": 1}
            ]
        }
        
        signals = []
        jobs = mock_jobs.get(company_name, [])
        
        for job in jobs:
            signals.append({
                "type": SignalType.HIRING.value,
                "description": f"Hiring: {job['title']}",
                "confidence": 85,
                "source": "LinkedIn Jobs",
                "detected_at": datetime.now() - timedelta(days=job["days_ago"]),
                "metadata": {
                    "role": job["title"],
                    "seniority": self._determine_seniority(job["title"])
                }
            })
        
        return signals
    
    async def _check_career_page(self, website: str) -> List[Dict[str, Any]]:
        """Check company career page for job postings"""
        # This would be a real web scraper in production
        return []
    
    def _get_mock_funding_data(self, company_name: str) -> Optional[Dict[str, Any]]:
        """Mock funding data for demonstration"""
        mock_funding = {
            "TechScale Inc": {
                "description": "Raised $10M Series A funding",
                "confidence": 90,
                "amount": "$10M",
                "round": "Series A",
                "date": (datetime.now() - timedelta(days=45)).isoformat()
            },
            "StartupXYZ": {
                "description": "Secured $2M seed funding",
                "confidence": 85,
                "amount": "$2M",
                "round": "Seed",
                "date": (datetime.now() - timedelta(days=90)).isoformat()
            }
        }
        
        return mock_funding.get(company_name)
    
    def _get_mock_company_news(self, company_name: str) -> List[Dict[str, Any]]:
        """Mock company news for demonstration"""
        mock_news = {
            "TechScale Inc": [
                {
                    "title": "Expanding to European market",
                    "confidence": 80,
                    "source": "TechCrunch",
                    "days_ago": 30,
                    "category": "expansion"
                }
            ],
            "GrowthLab SaaS": [
                {
                    "title": "Launching new AI-powered marketing platform",
                    "confidence": 75,
                    "source": "Business Insider",
                    "days_ago": 15,
                    "category": "product_launch"
                }
            ]
        }
        
        return mock_news.get(company_name, [])
    
    def _analyze_tech_stack(self, html: str) -> List[str]:
        """Analyze HTML for technology indicators"""
        technologies = []
        
        # Check for common marketing/analytics tools
        tech_patterns = {
            "Google Analytics": r"google-analytics\.com|gtag\.js|ga\('create'",
            "HubSpot": r"hubspot|hs-script",
            "Marketo": r"marketo|munchkin",
            "Salesforce": r"salesforce|sfdc",
            "Intercom": r"intercom",
            "Segment": r"segment\.io",
            "Mixpanel": r"mixpanel",
            "Amplitude": r"amplitude",
            "Hotjar": r"hotjar",
            "Optimizely": r"optimizely"
        }
        
        for tech_name, pattern in tech_patterns.items():
            if re.search(pattern, html, re.IGNORECASE):
                technologies.append(tech_name)
        
        return technologies
    
    def _determine_seniority(self, job_title: str) -> str:
        """Determine seniority level from job title"""
        title_lower = job_title.lower()
        
        if any(word in title_lower for word in ["vp", "vice president", "chief", "director"]):
            return "executive"
        elif "manager" in title_lower or "lead" in title_lower:
            return "manager"
        elif "senior" in title_lower:
            return "senior"
        else:
            return "individual"
