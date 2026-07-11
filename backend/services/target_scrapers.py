import aiohttp
from bs4 import BeautifulSoup
import re
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class BusinessDirectoryScraper:
    """Scrape business directories for leads"""
    
    async def scrape_yellowpages(self, search_term: str, location: str = "") -> List[Dict]:
        """Scrape YellowPages for businesses"""
        url = f"https://www.yellowpages.com/search?search_terms={search_term}&geo_location_terms={location}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    leads = []
                    listings = soup.select('.result')
                    
                    for listing in listings[:20]:  # First 20 results
                        lead = {
                            'source': 'yellowpages',
                            'company_name': self._extract_text(listing, '.business-name'),
                            'phone': self._extract_text(listing, '.phones'),
                            'address': self._extract_text(listing, '.address'),
                            'website': self._extract_href(listing, '.links a.track-visit-website'),
                            'categories': self._extract_categories(listing),
                            'years_in_business': self._extract_years(listing),
                            'rating': self._extract_rating(listing)
                        }
                        
                        # Clean and validate
                        if lead['company_name'] and lead['phone']:
                            leads.append(lead)
                    
                    return leads
                    
        except Exception as e:
            logger.error(f"Error scraping YellowPages: {str(e)}")
            return []
    
    async def scrape_linkedin_companies(self, industry: str, location: str = "") -> List[Dict]:
        """Scrape LinkedIn company information"""
        # Note: LinkedIn requires authentication and has strict rate limits
        # Consider using their API instead of scraping
        
        url = f"https://www.linkedin.com/search/results/companies/?keywords={industry}&location={location}"
        
        # This is a simplified example - real implementation needs authentication
        sample_companies = [
            {
                'source': 'linkedin',
                'company_name': 'Digital Marketing Pro',
                'industry': 'Marketing and Advertising',
                'company_size': '11-50 employees',
                'headquarters': 'New York, NY',
                'specialties': 'SEO, Social Media, PPC',
                'follower_count': '1,234',
                'website': 'https://digitalmarketingpro.com'
            },
            {
                'source': 'linkedin',
                'company_name': 'Tech Growth Agency',
                'industry': 'Information Technology & Services',
                'company_size': '51-200 employees',
                'headquarters': 'San Francisco, CA',
                'specialties': 'SaaS, B2B, Growth Marketing',
                'follower_count': '5,678',
                'website': 'https://techgrowth.com'
            }
        ]
        
        return sample_companies
    
    async def scrape_clutch_agencies(self, service: str = "digital-marketing") -> List[Dict]:
        """Scrape Clutch.co for marketing agencies"""
        url = f"https://clutch.co/{service}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    agencies = []
                    agency_cards = soup.select('.provider-row')
                    
                    for card in agency_cards[:15]:
                        agency = {
                            'source': 'clutch',
                            'agency_name': self._extract_text(card, '.company_info a'),
                            'tagline': self._extract_text(card, '.tagline'),
                            'location': self._extract_text(card, '.locality'),
                            'hourly_rate': self._extract_text(card, '.hourly-rate'),
                            'min_project_size': self._extract_text(card, '.size'),
                            'employee_count': self._extract_text(card, '.employees'),
                            'rating': self._extract_text(card, '.rating'),
                            'review_count': self._extract_text(card, '.reviews'),
                            'services': self._extract_services(card),
                            'website': self._extract_href(card, '.website-link a')
                        }
                        
                        if agency['agency_name']:
                            agencies.append(agency)
                    
                    return agencies
                    
        except Exception as e:
            logger.error(f"Error scraping Clutch: {str(e)}")
            return []
    
    async def scrape_google_business(self, query: str, location: str = "") -> List[Dict]:
        """Scrape Google Business listings"""
        # Note: Google scraping requires careful handling of terms of service
        # Consider using Google Places API instead
        
        url = f"https://www.google.com/search?q={query}+{location}+business"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    businesses = []
                    # Google results have specific selectors
                    results = soup.select('.VkpGBb, .dbg0pd, .rlfl__tls')
                    
                    for result in results[:10]:
                        business = {
                            'source': 'google_business',
                            'name': self._extract_text(result, '.dbg0pd'),
                            'rating': self._extract_text(result, '.BTtC6e'),
                            'reviews': self._extract_text(result, '.hqzQac'),
                            'address': self._extract_text(result, '.rllt__details'),
                            'phone': self._extract_phone(html),
                            'hours': self._extract_text(result, '.WgFkxc'),
                            'website': self._extract_href(result, '.ab_button')
                        }
                        
                        if business['name']:
                            businesses.append(business)
                    
                    return businesses
                    
        except Exception as e:
            logger.error(f"Error scraping Google Business: {str(e)}")
            return []
    
    def _extract_text(self, element, selector: str) -> str:
        """Extract text from element using selector"""
        try:
            selected = element.select_one(selector)
            return selected.text.strip() if selected else ""
        except:
            return ""
    
    def _extract_href(self, element, selector: str) -> str:
        """Extract href attribute from element"""
        try:
            selected = element.select_one(selector)
            return selected.get('href', '') if selected else ""
        except:
            return ""
    
    def _extract_categories(self, element) -> List[str]:
        """Extract business categories"""
        try:
            cats = element.select('.categories a')
            return [cat.text.strip() for cat in cats]
        except:
            return []
    
    def _extract_years(self, element) -> str:
        """Extract years in business"""
        try:
            text = element.text
            # Look for patterns like "in business 15 years"
            match = re.search(r'(\d+)\s+years', text, re.IGNORECASE)
            return match.group(1) if match else ""
        except:
            return ""
    
    def _extract_rating(self, element) -> float:
        """Extract numeric rating"""
        try:
            rating_text = self._extract_text(element, '.rating')
            # Extract number from "4.5 stars"
            match = re.search(r'(\d+\.?\d*)', rating_text)
            return float(match.group(1)) if match else 0.0
        except:
            return 0.0
    
    def _extract_services(self, element) -> List[str]:
        """Extract services offered"""
        try:
            services = element.select('.chart-label')
            return [s.text.strip() for s in services]
        except:
            return []
    
    def _extract_phone(self, html: str) -> str:
        """Extract phone number from text"""
        try:
            # Common phone pattern matching
            phone_patterns = [
                r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
                r'\+\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
            ]
            
            for pattern in phone_patterns:
                match = re.search(pattern, html)
                if match:
                    return match.group(0)
            return ""
        except:
            return ""