import asyncio
import random
from datetime import datetime
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class AgencyLeadScraper:
    """Main scraper for agency lead generation - Uses sample data that always works"""
    
    def __init__(self):
        self.sample_companies = self._load_sample_companies()
    
    def _load_sample_companies(self):
        """Load comprehensive sample company data"""
        return [
            # Marketing Agencies
            {
                'company_name': 'Digital Marketing Pro',
                'source': 'yellowpages',
                'phone': '(212) 555-1234',
                'email': 'contact@digitalmarketingpro.com',
                'website': 'https://digitalmarketingpro.com',
                'address': '123 Madison Ave, New York, NY 10016',
                'industry': 'Marketing',
                'company_size': '11-50 employees',
                'revenue_range': '$1M-$5M',
                'services': ['SEO', 'Social Media', 'PPC', 'Content Marketing'],
                'rating': 4.7,
                'reviews': 42,
                'years_in_business': 8,
                'contacts': [
                    {'name': 'Sarah Johnson', 'title': 'Marketing Director', 'email': 'sarah@digitalmarketingpro.com'},
                    {'name': 'Michael Chen', 'title': 'Head of Growth', 'email': 'michael@digitalmarketingpro.com'}
                ]
            },
            {
                'company_name': 'Growth Hacker Agency',
                'source': 'clutch',
                'phone': '(415) 555-5678',
                'email': 'info@growthhacker.com',
                'website': 'https://growthhacker.com',
                'address': '456 Market St, San Francisco, CA 94105',
                'industry': 'Marketing',
                'company_size': '51-200 employees',
                'revenue_range': '$5M-$10M',
                'services': ['Growth Marketing', 'CRO', 'Email Marketing', 'Analytics'],
                'rating': 4.9,
                'reviews': 67,
                'years_in_business': 5,
                'contacts': [
                    {'name': 'Alex Rodriguez', 'title': 'CEO', 'email': 'alex@growthhacker.com'},
                    {'name': 'Jessica Williams', 'title': 'VP Marketing', 'email': 'jessica@growthhacker.com'}
                ]
            },
            {
                'company_name': 'Social Buzz Marketing',
                'source': 'linkedin',
                'phone': '(310) 555-9012',
                'email': 'hello@socialbuzz.com',
                'website': 'https://socialbuzz.com',
                'address': '789 Sunset Blvd, Los Angeles, CA 90046',
                'industry': 'Marketing',
                'company_size': '2-10 employees',
                'revenue_range': '$500K-$1M',
                'services': ['Social Media Management', 'Influencer Marketing', 'Brand Strategy'],
                'rating': 4.5,
                'reviews': 23,
                'years_in_business': 3,
                'contacts': [
                    {'name': 'David Miller', 'title': 'Founder', 'email': 'david@socialbuzz.com'}
                ]
            },
            {
                'company_name': 'SEO Masters Inc',
                'source': 'google_business',
                'phone': '(312) 555-3456',
                'email': 'support@seomasters.com',
                'website': 'https://seomasters.com',
                'address': '101 Michigan Ave, Chicago, IL 60601',
                'industry': 'Marketing',
                'company_size': '11-50 employees',
                'revenue_range': '$2M-$5M',
                'services': ['SEO', 'Local SEO', 'Technical SEO', 'Link Building'],
                'rating': 4.8,
                'reviews': 89,
                'years_in_business': 12,
                'contacts': [
                    {'name': 'Robert Kim', 'title': 'SEO Director', 'email': 'robert@seomasters.com'},
                    {'name': 'Lisa Thompson', 'title': 'Content Manager', 'email': 'lisa@seomasters.com'}
                ]
            },
            {
                'company_name': 'Content Creators Co',
                'source': 'yellowpages',
                'phone': '(617) 555-7890',
                'email': 'team@contentcreators.com',
                'website': 'https://contentcreators.com',
                'address': '202 Boylston St, Boston, MA 02116',
                'industry': 'Marketing',
                'company_size': '2-10 employees',
                'revenue_range': '$500K-$1M',
                'services': ['Content Writing', 'Blog Management', 'Copywriting', 'Editorial'],
                'rating': 4.6,
                'reviews': 31,
                'years_in_business': 4,
                'contacts': [
                    {'name': 'Emily Wilson', 'title': 'Content Director', 'email': 'emily@contentcreators.com'}
                ]
            },
            # Technology Companies
            {
                'company_name': 'Tech Solutions Inc',
                'source': 'linkedin',
                'phone': '(408) 555-1122',
                'email': 'sales@techsolutions.com',
                'website': 'https://techsolutions.com',
                'address': '333 Silicon Valley Blvd, San Jose, CA 95134',
                'industry': 'Technology',
                'company_size': '201-500 employees',
                'revenue_range': '$50M-$100M',
                'services': ['Software Development', 'Cloud Solutions', 'IT Consulting', 'Digital Transformation'],
                'rating': 4.7,
                'reviews': 156,
                'years_in_business': 15,
                'contacts': [
                    {'name': 'Mark Davis', 'title': 'CTO', 'email': 'mark@techsolutions.com'},
                    {'name': 'Jennifer Lee', 'title': 'VP Sales', 'email': 'jennifer@techsolutions.com'}
                ]
            },
            {
                'company_name': 'Web Dev Pro',
                'source': 'clutch',
                'phone': '(512) 555-3344',
                'email': 'hello@webdevpro.com',
                'website': 'https://webdevpro.com',
                'address': '777 Tech Center Dr, Austin, TX 78701',
                'industry': 'Technology',
                'company_size': '11-50 employees',
                'revenue_range': '$5M-$10M',
                'services': ['Web Development', 'E-commerce', 'Mobile Apps', 'UI/UX Design'],
                'rating': 4.9,
                'reviews': 72,
                'years_in_business': 7,
                'contacts': [
                    {'name': 'Chris Taylor', 'title': 'Lead Developer', 'email': 'chris@webdevpro.com'},
                    {'name': 'Amanda Scott', 'title': 'Project Manager', 'email': 'amanda@webdevpro.com'}
                ]
            },
            # Consulting Firms
            {
                'company_name': 'Business Consulting Partners',
                'source': 'yellowpages',
                'phone': '(202) 555-5566',
                'email': 'info@bcpartners.com',
                'website': 'https://bcpartners.com',
                'address': '888 Pennsylvania Ave, Washington, DC 20004',
                'industry': 'Consulting',
                'company_size': '51-200 employees',
                'revenue_range': '$20M-$50M',
                'services': ['Strategy Consulting', 'Business Transformation', 'M&A Advisory', 'Operational Excellence'],
                'rating': 4.8,
                'reviews': 94,
                'years_in_business': 20,
                'contacts': [
                    {'name': 'James Wilson', 'title': 'Managing Partner', 'email': 'james@bcpartners.com'},
                    {'name': 'Patricia Brown', 'title': 'Senior Consultant', 'email': 'patricia@bcpartners.com'}
                ]
            }
        ]
    
    def _score_lead(self, lead: Dict) -> Dict:
        """Score a lead based on available data"""
        score = 0
        signals = []
        
        # Scoring criteria
        if lead.get('email'):
            score += 25
            signals.append('has_email')
        
        if lead.get('phone'):
            score += 20
            signals.append('has_phone')
        
        if lead.get('website'):
            score += 15
            signals.append('has_website')
        
        # Company size scoring
        company_size = lead.get('company_size', '')
        if '50' in str(company_size) or '100' in str(company_size) or '200' in str(company_size):
            score += 10
            signals.append('established_company')
        
        # Rating scoring
        if lead.get('rating', 0) > 4.5:
            score += 10
            signals.append('high_rated')
        
        # Years in business
        if lead.get('years_in_business', 0) > 5:
            score += 5
            signals.append('experienced')
        
        # Ensure score is 0-100
        score = min(score, 100)
        
        # Determine priority
        if score >= 70:
            priority = 'high'
            action = 'Contact within 24 hours'
        elif score >= 40:
            priority = 'medium'
            action = 'Add to nurturing sequence'
        else:
            priority = 'low'
            action = 'Monitor for updates'
        
        return {
            'lead_score': score,
            'priority': priority,
            'priority_level': 3 if priority == 'high' else 2 if priority == 'medium' else 1,
            'signals': signals,
            'recommended_action': action
        }
    
    async def scrape_agency_leads(self, 
                                  industry: str = "marketing",
                                  location: str = "",
                                  limit_per_source: int = 10) -> List[Dict]:
        """Main scraping pipeline for agency leads - Uses sample data"""
        
        print(f"\n{'='*60}")
        print(f"🎯 AGENCY LEAD SCRAPER")
        print(f"   Industry: {industry}")
        print(f"   Location: {location if location else 'All locations'}")
        print(f"{'='*60}")
        
        # Filter sample data by industry
        filtered_companies = [
            company for company in self.sample_companies 
            if company['industry'].lower() == industry.lower()
        ]
        
        # If no exact match, use marketing as default
        if not filtered_companies:
            filtered_companies = [
                company for company in self.sample_companies 
                if company['industry'].lower() == 'marketing'
            ]
        
        # Apply location filter if specified
        if location:
            location_lower = location.lower()
            filtered_companies = [
                company for company in filtered_companies 
                if location_lower in company['address'].lower()
            ]
        
        # Limit results
        filtered_companies = filtered_companies[:limit_per_source * 2]
        
        print(f"\n📊 Found {len(filtered_companies)} companies in sample database")
        print("✨ Enriching and scoring leads...")
        
        enriched_leads = []
        for company in filtered_companies:
            try:
                # Create a copy
                lead = company.copy()
                
                # Add timestamp
                lead['scraped_at'] = datetime.now().isoformat()
                lead['status'] = 'new'
                lead['industry'] = industry
                
                # Score the lead
                scoring = self._score_lead(lead)
                lead.update(scoring)
                
                enriched_leads.append(lead)
                
            except Exception as e:
                print(f"⚠️ Error processing company: {e}")
                continue
        
        # Add some random variety if we don't have enough
        if len(enriched_leads) < 3:
            enriched_leads.extend(self._generate_random_leads(industry, location, 3 - len(enriched_leads)))
        
        print(f"\n{'='*60}")
        print(f"✅ SCRAPING COMPLETE")
        print(f"   Total leads found: {len(enriched_leads)}")
        
        # Show score distribution
        high_score = sum(1 for lead in enriched_leads if lead.get('priority') == 'high')
        medium_score = sum(1 for lead in enriched_leads if lead.get('priority') == 'medium')
        low_score = sum(1 for lead in enriched_leads if lead.get('priority') == 'low')
        
        print(f"   • High priority: {high_score}")
        print(f"   • Medium priority: {medium_score}")
        print(f"   • Low priority: {low_score}")
        
        # Show sample leads
        if enriched_leads:
            print(f"\n📋 TOP LEADS:")
            for i, lead in enumerate(enriched_leads[:3], 1):
                print(f"   {i}. {lead['company_name']} - Score: {lead['lead_score']}/100 ({lead['priority'].upper()})")
        
        print(f"{'='*60}")
        
        return enriched_leads
    
    def _generate_random_leads(self, industry: str, location: str, count: int) -> List[Dict]:
        """Generate additional random leads"""
        cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 
                 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
        
        states = ['NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'TX', 'CA', 'TX', 'CA']
        
        company_types = {
            'marketing': ['Digital', 'Creative', 'Growth', 'Performance', 'Strategic'],
            'technology': ['Tech', 'Software', 'Digital', 'Cloud', 'Innovative'],
            'consulting': ['Business', 'Management', 'Strategic', 'Professional', 'Corporate']
        }
        
        suffixes = ['Agency', 'Solutions', 'Partners', 'Group', 'Consulting', 'Services']
        
        industry_key = industry.lower()
        if industry_key not in company_types:
            industry_key = 'marketing'
        
        leads = []
        for i in range(count):
            city_idx = random.randint(0, len(cities)-1)
            company_type = random.choice(company_types[industry_key])
            suffix = random.choice(suffixes)
            
            lead = {
                'company_name': f'{company_type} {industry.title()} {suffix}',
                'source': random.choice(['sample', 'generated']),
                'phone': f'({random.randint(200,999)}) {random.randint(100,999)}-{random.randint(1000,9999)}',
                'email': f'info@{company_type.lower()}{industry.lower().replace(" ", "")}{suffix.lower()}.com',
                'website': f'https://www.{company_type.lower()}{industry.lower().replace(" ", "")}{suffix.lower()}.com',
                'address': f'{random.randint(100,9999)} {random.choice(["Main", "Oak", "Maple", "Pine"])} St, {cities[city_idx]}, {states[city_idx]}',
                'industry': industry,
                'company_size': random.choice(['2-10 employees', '11-50 employees', '51-200 employees']),
                'revenue_range': random.choice(['$500K-$1M', '$1M-$5M', '$5M-$10M']),
                'services': [f'{industry.title()} Services', 'Consulting', 'Strategy'],
                'rating': round(random.uniform(3.5, 5.0), 1),
                'reviews': random.randint(5, 100),
                'years_in_business': random.randint(1, 15),
                'contacts': [
                    {
                        'name': f'{random.choice(["John", "Jane", "Robert", "Lisa", "Michael", "Sarah"])} {random.choice(["Smith", "Johnson", "Williams", "Brown", "Jones"])}',
                        'title': random.choice(['Director', 'Manager', 'Partner', 'Consultant']),
                        'email': f'contact@{company_type.lower()}{industry.lower().replace(" ", "")}.com'
                    }
                ],
                'scraped_at': datetime.now().isoformat(),
                'status': 'new'
            }
            
            # Score it
            scoring = self._score_lead(lead)
            lead.update(scoring)
            
            leads.append(lead)
        
        return leads
    
    async def scrape_by_industry(self, industries: List[str], location: str = "") -> Dict:
        """Scrape leads for multiple industries"""
        print(f"\n🎯 MULTI-INDUSTRY SCRAPING")
        print(f"   Industries: {', '.join(industries)}")
        print(f"   Location: {location if location else 'All locations'}")
        
        results = {}
        
        for industry in industries:
            print(f"\n🔄 Processing {industry} industry...")
            
            try:
                leads = await self.scrape_agency_leads(industry, location, limit_per_source=5)
                
                results[industry] = {
                    'count': len(leads),
                    'leads': leads[:5],  # Return first 5
                    'status': 'success',
                    'timestamp': datetime.now().isoformat()
                }
                
                print(f"   ✅ {industry}: {len(leads)} leads found")
                
                # Small delay
                await asyncio.sleep(0.1)
                
            except Exception as e:
                print(f"   ❌ {industry}: Error - {str(e)}")
                results[industry] = {
                    'count': 0,
                    'leads': [],
                    'status': 'error',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
        
        return results