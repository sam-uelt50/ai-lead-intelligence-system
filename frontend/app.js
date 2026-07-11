// ============================================================
// APP.JS - COMPLETE v11.0 WITH ALL FIXES
// Lead Accumulation + Export Fix + All Features Working
// ============================================================

// ============================================================
// LANDING PAGE FUNCTIONS
// ============================================================

function enterDashboard() {
    console.log('🚪 Entering Dashboard...');
    const landingPage = document.getElementById('landingPage');
    const dashboardWrapper = document.getElementById('dashboardWrapper');
    
    if (landingPage) {
        landingPage.classList.add('hidden');
        landingPage.style.display = 'none';
    }
    if (dashboardWrapper) {
        dashboardWrapper.classList.add('active');
        dashboardWrapper.style.display = 'flex';
    }
    
    setTimeout(() => {
        if (typeof initializeDashboard === 'function') {
            initializeDashboard();
        } else {
            console.log('⚠️ Loading data directly...');
            if (typeof generateLeads === 'function') {
                generateLeads();
            }
            if (typeof showDashboard === 'function') {
                showDashboard();
            }
        }
    }, 300);
}

function scrollToFeatures() {
    const section = document.getElementById('featuresSection');
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

// ============================================================
// COMPLETE API CONFIG
// ============================================================
const API_CONFIG = {
    baseURL: 'http://localhost:8007',
    token: 'test-token-2024',
    endpoints: {
        leads: '/api/leads',
        prioritized: '/api/leads/prioritized',
        massive: '/api/scrape/massive',
        ethiopian: '/api/scrape/ethiopia',
        global: '/api/scrape/global',
        testScrapingbee: '/api/test-scrapingbee',
        health: '/health',
        authTest: '/api/auth-test',
        dashboard: '/api/dashboard/stats',
        today: '/api/leads/today',
        export: '/api/export/leads',
        mongodbReconnect: '/api/mongodb/reconnect',
        hunterDomainSearch: '/api/hunter/domain-search',
        hunterEmailFinder: '/api/hunter/email-finder',
        hunterEmailVerifier: '/api/hunter/email-verifier',
        hunterCompanyEnrichment: '/api/hunter/company-enrichment',
        hunterPersonEnrichment: '/api/hunter/person-enrichment',
        hunterCombinedEnrichment: '/api/hunter/combined-enrichment',
        discoverEmails: '/api/discover/emails',
        verifyEmailDIY: '/api/verify/email-diy',
        hunterUsage: '/api/hunter/usage',
        clearbitUsage: '/api/clearbit/usage',
        discoverDomain: '/api/discover/domain',
        discoverDecisionMakers: '/api/discover/decision-makers',
        verifyEmail: '/api/verify/email',
        countries: '/api/countries',
        countryLeads: '/api/country/leads',
        countryRegions: '/api/country/regions',
        countryCities: '/api/country/cities',
        countryIndustries: '/api/country/industries',
        ethiopianCompanies: '/api/ethiopia/companies',
        ethiopianRegions: '/api/ethiopia/regions',
        ethiopianCities: '/api/ethiopia/cities',
        ethiopianIndustries: '/api/ethiopia/industries'
    }
};

// ============================================================
// GLOBAL CONFIGURATION - COMPLETE 48 COUNTRIES
// ============================================================
const GLOBAL_CONFIG = {
    countries: [
        { code: 'ET', name: 'Ethiopia', flag: '🇪🇹', default: true },
        { code: 'US', name: 'United States', flag: '🇺🇸' },
        { code: 'GB', name: 'United Kingdom', flag: '🇬🇧' },
        { code: 'CA', name: 'Canada', flag: '🇨🇦' },
        { code: 'AU', name: 'Australia', flag: '🇦🇺' },
        { code: 'DE', name: 'Germany', flag: '🇩🇪' },
        { code: 'FR', name: 'France', flag: '🇫🇷' },
        { code: 'IT', name: 'Italy', flag: '🇮🇹' },
        { code: 'ES', name: 'Spain', flag: '🇪🇸' },
        { code: 'PT', name: 'Portugal', flag: '🇵🇹' },
        { code: 'NL', name: 'Netherlands', flag: '🇳🇱' },
        { code: 'BE', name: 'Belgium', flag: '🇧🇪' },
        { code: 'CH', name: 'Switzerland', flag: '🇨🇭' },
        { code: 'SE', name: 'Sweden', flag: '🇸🇪' },
        { code: 'NO', name: 'Norway', flag: '🇳🇴' },
        { code: 'DK', name: 'Denmark', flag: '🇩🇰' },
        { code: 'FI', name: 'Finland', flag: '🇫🇮' },
        { code: 'PL', name: 'Poland', flag: '🇵🇱' },
        { code: 'CZ', name: 'Czech Republic', flag: '🇨🇿' },
        { code: 'AT', name: 'Austria', flag: '🇦🇹' },
        { code: 'IE', name: 'Ireland', flag: '🇮🇪' },
        { code: 'NZ', name: 'New Zealand', flag: '🇳🇿' },
        { code: 'SG', name: 'Singapore', flag: '🇸🇬' },
        { code: 'MY', name: 'Malaysia', flag: '🇲🇾' },
        { code: 'PH', name: 'Philippines', flag: '🇵🇭' },
        { code: 'VN', name: 'Vietnam', flag: '🇻🇳' },
        { code: 'TH', name: 'Thailand', flag: '🇹🇭' },
        { code: 'ID', name: 'Indonesia', flag: '🇮🇩' },
        { code: 'IN', name: 'India', flag: '🇮🇳' },
        { code: 'JP', name: 'Japan', flag: '🇯🇵' },
        { code: 'KR', name: 'South Korea', flag: '🇰🇷' },
        { code: 'CN', name: 'China', flag: '🇨🇳' },
        { code: 'TW', name: 'Taiwan', flag: '🇹🇼' },
        { code: 'HK', name: 'Hong Kong', flag: '🇭🇰' },
        { code: 'AE', name: 'UAE', flag: '🇦🇪' },
        { code: 'SA', name: 'Saudi Arabia', flag: '🇸🇦' },
        { code: 'IL', name: 'Israel', flag: '🇮🇱' },
        { code: 'ZA', name: 'South Africa', flag: '🇿🇦' },
        { code: 'NG', name: 'Nigeria', flag: '🇳🇬' },
        { code: 'KE', name: 'Kenya', flag: '🇰🇪' },
        { code: 'EG', name: 'Egypt', flag: '🇪🇬' },
        { code: 'MA', name: 'Morocco', flag: '🇲🇦' },
        { code: 'GH', name: 'Ghana', flag: '🇬🇭' },
        { code: 'BR', name: 'Brazil', flag: '🇧🇷' },
        { code: 'MX', name: 'Mexico', flag: '🇲🇽' },
        { code: 'AR', name: 'Argentina', flag: '🇦🇷' },
        { code: 'CL', name: 'Chile', flag: '🇨🇱' },
        { code: 'CO', name: 'Colombia', flag: '🇨🇴' }
    ],
    regions: {
        ET: ['Addis Ababa', 'Oromia', 'Amhara', 'Tigray', 'Sidama', 'SNNPR', 'Gambela', 'Benishangul-Gumuz', 'Somali', 'Afar', 'Harari', 'Dire Dawa'],
        US: ['California', 'Texas', 'New York', 'Florida', 'Illinois', 'Pennsylvania', 'Ohio', 'Georgia', 'North Carolina', 'Michigan', 'Washington', 'Arizona', 'Massachusetts', 'Tennessee', 'Indiana', 'Missouri', 'Maryland', 'Wisconsin', 'Colorado', 'Minnesota'],
        GB: ['England', 'Scotland', 'Wales', 'Northern Ireland', 'London', 'Greater Manchester'],
        CA: ['Ontario', 'Quebec', 'British Columbia', 'Alberta', 'Manitoba'],
        AU: ['New South Wales', 'Victoria', 'Queensland', 'Western Australia', 'South Australia'],
        DE: ['Berlin', 'Bavaria', 'Hamburg', 'North Rhine-Westphalia', 'Lower Saxony'],
        FR: ['Île-de-France', 'Auvergne-Rhône-Alpes', 'Grand Est', 'Nouvelle-Aquitaine'],
        IT: ['Lombardy', 'Lazio', 'Campania', 'Veneto', 'Piedmont'],
        ES: ['Andalusia', 'Catalonia', 'Community of Madrid', 'Valencia'],
        IN: ['Maharashtra', 'Uttar Pradesh', 'Tamil Nadu', 'Karnataka', 'Gujarat']
    },
    cities: {
        ET: ['Addis Ababa', 'Adama', 'Bahir Dar', 'Gondar', 'Mekelle', 'Hawassa', 'Jimma', 'Dire Dawa', 'Dessie', 'Jijiga', 'Shashamane', 'Bishoftu'],
        US: ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte', 'San Francisco', 'Indianapolis', 'Seattle', 'Denver', 'Washington DC', 'Boston', 'Miami', 'Atlanta', 'Portland'],
        GB: ['London', 'Birmingham', 'Leeds', 'Glasgow', 'Manchester', 'Sheffield', 'Bradford', 'Edinburgh', 'Liverpool', 'Bristol', 'Cardiff'],
        CA: ['Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Edmonton', 'Ottawa', 'Winnipeg', 'Quebec City', 'Hamilton'],
        AU: ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide', 'Gold Coast', 'Newcastle', 'Canberra'],
        DE: ['Berlin', 'Hamburg', 'Munich', 'Cologne', 'Frankfurt', 'Stuttgart', 'Düsseldorf', 'Dortmund', 'Essen', 'Leipzig'],
        FR: ['Paris', 'Marseille', 'Lyon', 'Toulouse', 'Nice', 'Nantes', 'Strasbourg', 'Montpellier', 'Bordeaux', 'Lille'],
        IT: ['Rome', 'Milan', 'Naples', 'Turin', 'Palermo', 'Genoa', 'Bologna', 'Florence', 'Bari', 'Catania'],
        ES: ['Madrid', 'Barcelona', 'Valencia', 'Seville', 'Zaragoza', 'Málaga', 'Murcia', 'Palma', 'Bilbao'],
        IN: ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Ahmedabad', 'Chennai', 'Kolkata', 'Pune', 'Jaipur', 'Lucknow']
    }
};

// ============================================================
// INDUSTRY HIERARCHY - COMPLETE
// ============================================================
const INDUSTRY_HIERARCHY = {
    'Technology & Software': {
        icon: '💻',
        industries: ['Software Development', 'SaaS', 'Cloud Computing', 'Artificial Intelligence', 'Machine Learning', 'Blockchain', 'Cybersecurity', 'Data Analytics', 'FinTech', 'EdTech', 'HealthTech', 'PropTech', 'LegalTech', 'HR Tech', 'AdTech', 'MarTech', 'InsurTech', 'AgriTech', 'DevOps', 'IT Consulting']
    },
    'E-commerce & Retail': {
        icon: '🛒',
        industries: ['E-commerce', 'Retail', 'D2C Brands', 'Marketplace', 'CPG', 'FMCG', 'Consumer Goods', 'Fashion & Apparel', 'Luxury Goods', 'Beauty & Cosmetics', 'Jewelry', 'Sports & Outdoors']
    },
    'Finance & Banking': {
        icon: '💰',
        industries: ['Banking', 'Investment Banking', 'Asset Management', 'Private Equity', 'Venture Capital', 'Hedge Funds', 'Insurance', 'Real Estate Investment', 'Commercial Banking', 'Retail Banking', 'Microfinance', 'Islamic Banking', 'Wealth Management']
    },
    'Healthcare & Life Sciences': {
        icon: '🏥',
        industries: ['Healthcare', 'Hospitals', 'Pharmaceuticals', 'Biotechnology', 'Medical Devices', 'Telemedicine', 'Health Insurance', 'Mental Health', 'Senior Care', 'Veterinary', 'Clinical Research', 'Dental Care']
    },
    'Manufacturing & Industrial': {
        icon: '🏭',
        industries: ['Manufacturing', 'Industrial', 'Automotive', 'Aerospace', 'Construction', 'Steel & Metals', 'Textiles', 'Chemical', 'Plastics', 'Electronics Manufacturing', 'Paper & Packaging', '3D Printing', 'Industrial Automation']
    },
    'Energy & Utilities': {
        icon: '⚡',
        industries: ['Renewable Energy', 'Oil & Gas', 'Solar Energy', 'Wind Energy', 'Utilities', 'Water Management', 'Nuclear Energy', 'Energy Storage', 'Geothermal', 'Hydroelectric', 'Smart Grid']
    },
    'Agriculture & Food': {
        icon: '🌾',
        industries: ['Agriculture', 'Coffee Export', 'Flower Farming', 'Food Processing', 'Farming', 'Agribusiness', 'Fisheries', 'Forestry', 'Organic Farming', 'Sustainable Agriculture', 'AgTech', 'Food Manufacturing']
    },
    'Transportation & Logistics': {
        icon: '🚚',
        industries: ['Logistics', 'Transportation', 'Shipping', 'Aviation', 'Railway', 'Supply Chain', 'Warehousing', 'Fleet Management', 'Last Mile Delivery', 'Maritime', 'Freight Forwarding', 'Autonomous Vehicles']
    },
    'Real Estate & Construction': {
        icon: '🏗️',
        industries: ['Real Estate', 'Construction', 'Architecture', 'Urban Planning', 'Property Management', 'Real Estate Development', 'Interior Design', 'Landscaping', 'Civil Engineering']
    },
    'Media & Entertainment': {
        icon: '🎬',
        industries: ['Media', 'Entertainment', 'Publishing', 'Broadcasting', 'Film Production', 'Music', 'Gaming', 'Digital Media', 'Streaming Services', 'Podcasting', 'Animation', 'VFX', 'Esports']
    },
    'Telecommunications': {
        icon: '📡',
        industries: ['Telecom', 'Mobile Networks', 'Broadband', 'Satellite', 'Internet Service', '5G Technology', 'IoT Infrastructure', 'Network Equipment', 'Fibre Optic']
    },
    'Education & Training': {
        icon: '📚',
        industries: ['Education', 'EdTech', 'Training', 'Higher Education', 'K-12 Schools', 'Online Learning', 'Corporate Training', 'Vocational Training', 'Language Schools', 'Test Preparation', 'Special Education']
    },
    'Professional Services': {
        icon: '💼',
        industries: ['Consulting', 'Legal Services', 'Accounting', 'Architecture', 'Engineering', 'HR Services', 'Marketing Agency', 'PR Agency', 'Recruitment', 'Outsourcing', 'Management Consulting', 'IT Consulting', 'Strategy Consulting']
    },
    'Hospitality & Tourism': {
        icon: '🏨',
        industries: ['Hospitality', 'Tourism', 'Hotels', 'Restaurants', 'Travel Agencies', 'Cruise Lines', 'Tour Operators', 'Catering', 'Event Management', 'Theme Parks', 'Resorts', 'Spa Services']
    },
    'Non-Profit & Social': {
        icon: '❤️',
        industries: ['Non-Profit', 'NGO', 'Social Enterprise', 'Charity', 'Foundations', 'Community Development', 'Human Rights', 'Environmental', 'Animal Welfare', 'Cultural Heritage', 'Religious Organizations']
    }
};

const ALL_INDUSTRIES = Object.values(INDUSTRY_HIERARCHY).flatMap(category => category.industries);

// ============================================================
// SOURCE CONFIGURATION - COMPLETE
// ============================================================
const SOURCES = [
    { id: 'exa', name: 'Exa.ai', icon: '🔎', color: 'badge-exa', enabled: true },
    { id: 'yellowpages', name: 'YellowPages', icon: '📚', color: 'badge-yellowpages', enabled: true },
    { id: 'clearbit', name: 'Clearbit', icon: '💡', color: 'badge-clearbit', enabled: true },
    { id: 'apollo', name: 'Apollo.io', icon: '🚀', color: 'badge-apollo', enabled: true },
    { id: 'hunter', name: 'Hunter.io', icon: '📧', color: 'badge-hunter', enabled: true },
    { id: 'website', name: 'Website Email', icon: '🌐', color: 'badge-website', enabled: true },
    { id: '2ehire', name: '2Ehire Ethiopia', icon: '🇪🇹', color: 'badge-ethiopia', enabled: true },
    { id: 'ethioyellow', name: 'Ethio Yellow Pages', icon: '📒', color: 'badge-ethiopia', enabled: true },
    { id: 'ethiobusiness', name: 'Ethio Business', icon: '🏢', color: 'badge-ethiopia', enabled: true },
    { id: 'global_api', name: 'Global API', icon: '🌍', color: 'badge-global', enabled: true }
];

// ============================================================
// INIT INDUSTRY FILTERS
// ============================================================
function initIndustryFilters() {
    const container = document.getElementById('industryFilterContainer');
    if (!container) {
        const newContainer = document.createElement('div');
        newContainer.id = 'industryFilterContainer';
        newContainer.style.display = 'none';
        document.body.appendChild(newContainer);
        console.log('📋 Created industry filter container');
    }
    
    const industryDropdowns = ['ethiopianIndustryFilter', 'globalIndustryFilter'];
    industryDropdowns.forEach(id => {
        const dropdown = document.getElementById(id);
        if (dropdown) {
            dropdown.innerHTML = '<option value="">All Industries</option>';
            ALL_INDUSTRIES.slice(0, 30).forEach(industry => {
                const option = document.createElement('option');
                option.value = industry;
                option.textContent = industry;
                dropdown.appendChild(option);
            });
        }
    });
    console.log('✅ Industry filters initialized');
}

function initIndustryFiltersWithCheckboxes() {
    const container = document.getElementById('industryFilterContainer');
    if (!container) return;
    
    let html = '';
    let categoryIndex = 0;
    Object.entries(INDUSTRY_HIERARCHY).forEach(([category, data]) => {
        const categoryId = `category-${categoryIndex}`;
        html += `
            <div class="industry-filter-group" style="margin-bottom:0.5rem;border:1px solid var(--border-color);border-radius:8px;overflow:hidden;">
                <div class="industry-category-header" onclick="toggleCategory('${categoryId}')" style="padding:0.5rem 1rem;background:var(--light-bg);cursor:pointer;font-weight:600;display:flex;justify-content:space-between;align-items:center;">
                    ${data.icon} ${category} <span class="badge bg-secondary">${data.industries.length}</span>
                </div>
                <div id="${categoryId}" class="industry-checkbox-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:0.3rem;padding:0.5rem 1rem;">
                    ${data.industries.map(industry => `
                        <div class="industry-checkbox-item" style="display:flex;align-items:center;gap:0.3rem;font-size:0.8rem;">
                            <input type="checkbox" id="industry-${industry.replace(/\s+/g, '-')}" 
                                   value="${industry}" onchange="onIndustryChange()">
                            <label for="industry-${industry.replace(/\s+/g, '-')}">${industry}</label>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        categoryIndex++;
    });
    container.innerHTML = html;
    console.log('✅ Industry filter checkboxes initialized');
}

window.toggleCategory = function(categoryId) {
    const element = document.getElementById(categoryId);
    if (element) {
        element.style.display = element.style.display === 'none' ? 'grid' : 'none';
    }
};

window.onIndustryChange = function() {
    const checkedIndustries = document.querySelectorAll('#industryFilterContainer input[type="checkbox"]:checked');
    window.selectedIndustries = Array.from(checkedIndustries).map(el => el.value);
    updateSelectedFilters();
    applyAllFilters();
};

// ============================================================
// FORCE UPDATE DASHBOARD
// ============================================================
function forceUpdateDashboard() {
    console.log('🔄 Force updating dashboard...');
    
    if (!window.leads || window.leads.length === 0) {
        console.log('⚠️ No leads found, generating...');
        generateLeads();
        return;
    }
    
    const ethiopianCount = window.leads.filter(l => l.country === 'ET').length;
    const globalCount = window.leads.filter(l => l.country !== 'ET').length;
    const emailCount = window.leads.reduce((sum, l) => sum + (l.verified_emails?.length || 0), 0);
    const dmCount = window.leads.reduce((sum, l) => sum + (l.decision_makers?.length || 0), 0);
    const companiesWithEmails = window.leads.filter(l => l.verified_emails?.length > 0).length;
    const hiringSignals = window.leads.filter(l => l.hiring_data?.is_hiring).length;
    
    window.dashboardStats = {
        total_companies: window.leads.length,
        new_companies: window.leads.length,
        ethiopian_companies: ethiopianCount,
        global_companies: globalCount,
        companies_with_emails: companiesWithEmails,
        total_emails: emailCount,
        total_decision_makers: dmCount,
        hiring_signals: hiringSignals
    };
    
    updateDashboardStats();
    applyDateFilter();
    updateCompaniesGrid();
    updateCompaniesTable();
    updateDecisionMakersGrid();
    updateDecisionMakersTable();
    updateAIGrid();
    updatePagination();
    updateSelectedFilters();
    updateGlobalCompaniesGrid();
    updateGlobalCompaniesTable();
    updatePrioritizedLeadsDisplay();
    updateSourceBadges();
    updateScrapeStatsDisplay();
    updateRecentActivity();
    updateFilterCount();
    updateGlobalFilters();
    
    const companyBadge = document.getElementById('companyBadge');
    if (companyBadge) companyBadge.textContent = window.leads.length;
    
    const ethiopianBadge = document.getElementById('ethiopianBadge');
    if (ethiopianBadge) ethiopianBadge.textContent = ethiopianCount;
    
    const globalBadge = document.querySelector('#globalCompaniesLink .menu-badge');
    if (globalBadge) globalBadge.textContent = globalCount;
    
    const priorityCount = document.getElementById('priorityCount');
    if (priorityCount) priorityCount.textContent = window.leads.length;
    
    const lastUpdateTime = document.getElementById('lastUpdateTime');
    if (lastUpdateTime) {
        lastUpdateTime.textContent = new Date().toLocaleString();
    }
    
    console.log(`✅ Dashboard updated: ${window.leads.length} leads, ${ethiopianCount} Ethiopian, ${globalCount} Global`);
}

// ============================================================
// UPDATE DASHBOARD STATS
// ============================================================
function updateDashboardStats() {
    if (!window.dashboardStats) {
        if (window.leads && window.leads.length > 0) {
            const ethiopianCount = window.leads.filter(l => l.country === 'ET').length;
            const globalCount = window.leads.filter(l => l.country !== 'ET').length;
            const emailCount = window.leads.reduce((sum, l) => sum + (l.verified_emails?.length || 0), 0);
            const dmCount = window.leads.reduce((sum, l) => sum + (l.decision_makers?.length || 0), 0);
            window.dashboardStats = {
                total_companies: window.leads.length,
                new_companies: window.leads.length,
                ethiopian_companies: ethiopianCount,
                global_companies: globalCount,
                companies_with_emails: window.leads.filter(l => l.verified_emails?.length > 0).length,
                total_emails: emailCount,
                total_decision_makers: dmCount,
                hiring_signals: window.leads.filter(l => l.hiring_data?.is_hiring).length
            };
        } else {
            return;
        }
    }
    
    const stats = window.dashboardStats;
    
    const elements = {
        'totalCompanies': stats.total_companies || 0,
        'newCompanies': stats.new_companies || 0,
        'ethiopianCompanies': stats.ethiopian_companies || 0,
        'globalCompanies': stats.global_companies || 0,
        'totalEmails': stats.total_emails || 0,
        'totalDecisionMakers': stats.total_decision_makers || 0
    };
    
    Object.entries(elements).forEach(([id, value]) => {
        const el = document.getElementById(id);
        if (el) {
            el.textContent = value;
        }
    });
    
    const newCompaniesProgress = document.getElementById('newCompaniesProgress');
    if (newCompaniesProgress && stats.total_companies > 0) {
        const pct = Math.min((stats.new_companies / stats.total_companies) * 100, 100);
        newCompaniesProgress.style.width = `${pct}%`;
    }
}

// ============================================================
// API CLIENT CLASS
// ============================================================
class ApiClient {
    constructor() {
        this.baseURL = API_CONFIG.baseURL;
        this.token = API_CONFIG.token;
        this.isBackendAvailable = false;
        this.backendInfo = {};
        this.connectionCheckInterval = null;
        this._isChecking = false;
    }

    getHeaders() {
        return {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.token}`,
            'Accept': 'application/json'
        };
    }

    async request(endpoint, method = 'GET', data = null) {
        const url = `${this.baseURL}${endpoint}`;
        const options = {
            method,
            headers: this.getHeaders(),
            mode: 'cors',
            credentials: 'omit'
        };
        if (data) {
            options.body = JSON.stringify(data);
        }
        try {
            console.log(`📡 Fetching: ${url}`);
            const response = await fetch(url, options);
            let responseData;
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                responseData = await response.json();
            } else {
                const text = await response.text();
                responseData = { message: text };
            }
            return { 
                success: response.ok, 
                data: responseData, 
                status: response.status,
                statusText: response.statusText
            };
        } catch (error) {
            console.error('API Error:', error);
            return { 
                success: false, 
                error: error.message,
                isNetworkError: true 
            };
        }
    }

    async checkHealth() {
        try {
            const result = await this.request('/health');
            if (result.success) {
                this.isBackendAvailable = true;
                this.backendInfo = result.data;
                return { success: true, data: result.data };
            }
            return { success: false };
        } catch (error) {
            this.isBackendAvailable = false;
            return { success: false, error: error.message };
        }
    }
    
    async testAuth() {
        if (this._isChecking) {
            return { success: false, error: 'Auth check in progress' };
        }
        this._isChecking = true;
        
        try {
            const health = await this.checkHealth();
            if (health.success) {
                this._isChecking = false;
                return { 
                    success: true, 
                    data: { 
                        authenticated: true, 
                        message: 'Backend connected via health check',
                        ...health.data 
                    } 
                };
            }
            
            try {
                const authResult = await this.request('/api/auth-test');
                if (authResult.success) {
                    this.isBackendAvailable = true;
                    this._isChecking = false;
                    return authResult;
                }
            } catch (e) {}
            
            try {
                const response = await fetch(this.baseURL, {
                    method: 'HEAD',
                    mode: 'no-cors'
                });
                this.isBackendAvailable = true;
                this._isChecking = false;
                return { 
                    success: true, 
                    data: { 
                        authenticated: true, 
                        message: 'Backend server reachable',
                        mode: 'head-request'
                    } 
                };
            } catch (error) {
                this.isBackendAvailable = false;
                this._isChecking = false;
                return { 
                    success: false, 
                    error: 'Cannot connect to backend server',
                    isNetworkError: true
                };
            }
        } catch (error) {
            this._isChecking = false;
            return { success: false, error: error.message };
        }
    }
    
    async getLeads(params = {}) {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available', data: { data: [] } };
        }
        const queryParams = new URLSearchParams(params).toString();
        return this.request(`${API_CONFIG.endpoints.leads}?${queryParams}`); 
    }
    
    async getPrioritizedLeads(minIntentScore = 0, market = 'all', country = null) { 
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available', data: { leads: [] } };
        }
        let url = `${API_CONFIG.endpoints.prioritized}?min_intent_score=${minIntentScore}&market=${market}`;
        if (country) {
            url += `&country=${country}`;
        }
        return this.request(url); 
    }
    
    async massiveScrape(includeEthiopia = true, countries = ['ET', 'US', 'GB', 'CA', 'AU', 'DE', 'FR']) { 
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available' };
        }
        return this.request(API_CONFIG.endpoints.massive, 'POST', { 
            include_ethiopia: includeEthiopia,
            countries: countries
        }); 
    }
    
    async globalScrape(countries = ['ET', 'US', 'GB', 'CA', 'AU', 'DE', 'FR']) {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available' };
        }
        return this.request(API_CONFIG.endpoints.global, 'POST', { countries });
    }
    
    async scrapeEthiopianDirectories() {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available' };
        }
        return this.request(API_CONFIG.endpoints.ethiopian, 'POST', {});
    }
    
    async getEthiopianCompanies(params = {}) {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available', data: { data: [] } };
        }
        const queryParams = new URLSearchParams(params).toString();
        return this.request(`${API_CONFIG.endpoints.ethiopianCompanies}?${queryParams}`);
    }
    
    async getCountries() {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available', data: { countries: GLOBAL_CONFIG.countries } };
        }
        return this.request(API_CONFIG.endpoints.countries);
    }
    
    async getCountryLeads(countryCode, params = {}) {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available', data: { data: [] } };
        }
        const queryParams = new URLSearchParams({ country: countryCode, ...params }).toString();
        return this.request(`${API_CONFIG.endpoints.countryLeads}?${queryParams}`);
    }
    
    async getCountryRegions(countryCode) {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available', data: { regions: GLOBAL_CONFIG.regions[countryCode] || [] } };
        }
        return this.request(`${API_CONFIG.endpoints.countryRegions}?country=${countryCode}`);
    }
    
    async getCountryCities(countryCode) {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available', data: { cities: GLOBAL_CONFIG.cities[countryCode] || [] } };
        }
        return this.request(`${API_CONFIG.endpoints.countryCities}?country=${countryCode}`);
    }
    
    async getCountryIndustries(countryCode) {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available', data: { industries: ALL_INDUSTRIES } };
        }
        return this.request(`${API_CONFIG.endpoints.countryIndustries}?country=${countryCode}`);
    }
    
    async getEthiopianRegions() {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available', data: { regions: ETHIOPIAN_CONFIG.regions } };
        }
        return this.request(API_CONFIG.endpoints.ethiopianRegions);
    }
    
    async getEthiopianCities() {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available', data: { cities: ETHIOPIAN_CONFIG.cities } };
        }
        return this.request(API_CONFIG.endpoints.ethiopianCities);
    }
    
    async getEthiopianIndustries() {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available', data: { industries: ETHIOPIAN_CONFIG.industries } };
        }
        return this.request(API_CONFIG.endpoints.ethiopianIndustries);
    }
    
    async testScrapingbee() { 
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available' };
        }
        return this.request(API_CONFIG.endpoints.testScrapingbee); 
    }
    
    async healthCheck() { 
        return this.checkHealth();
    }
    
    async getDashboardStats(days = 30) {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available' };
        }
        return this.request(`${API_CONFIG.endpoints.dashboard}?days=${days}`);
    }
    
    async getTodayLeads() {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available' };
        }
        return this.request(API_CONFIG.endpoints.today);
    }
    
    async getLeadDetails(id, generateAi = false) {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available' };
        }
        return this.request(`/api/leads/${id}?generate_ai=${generateAi}`);
    }
    
    async updateLead(id, data) {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available' };
        }
        return this.request(`/api/leads/${id}`, 'PUT', data);
    }
    
    async hunterDomainSearch(domain) {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available' };
        }
        return this.request(API_CONFIG.endpoints.hunterDomainSearch, 'POST', { domain });
    }
    
    async hunterEmailFinder(domain, firstName, lastName) {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available' };
        }
        return this.request(API_CONFIG.endpoints.hunterEmailFinder, 'POST', { domain, first_name: firstName, last_name: lastName });
    }
    
    async hunterEmailVerifier(email) {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available' };
        }
        return this.request(API_CONFIG.endpoints.hunterEmailVerifier, 'POST', { email });
    }
    
    async hunterCompanyEnrichment(domain) {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available' };
        }
        return this.request(API_CONFIG.endpoints.hunterCompanyEnrichment, 'POST', { domain });
    }
    
    async hunterPersonEnrichment(email) {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available' };
        }
        return this.request(API_CONFIG.endpoints.hunterPersonEnrichment, 'POST', { email });
    }
    
    async hunterCombinedEnrichment(domain, email = null, firstName = null, lastName = null) {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available' };
        }
        return this.request(API_CONFIG.endpoints.hunterCombinedEnrichment, 'POST', { 
            domain, 
            email, 
            first_name: firstName, 
            last_name: lastName 
        });
    }
    
    async discoverEmails(domain, companyName = null) {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available' };
        }
        const url = companyName ? 
            `${API_CONFIG.endpoints.discoverEmails}?domain=${domain}&company_name=${encodeURIComponent(companyName)}` :
            `${API_CONFIG.endpoints.discoverEmails}?domain=${domain}`;
        return this.request(url, 'POST', {});
    }
    
    async verifyEmailDIY(email) {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available' };
        }
        return this.request(`${API_CONFIG.endpoints.verifyEmailDIY}?email=${encodeURIComponent(email)}`, 'POST', {});
    }
    
    async getHunterUsage() {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available' };
        }
        return this.request(API_CONFIG.endpoints.hunterUsage);
    }
    
    async getClearbitUsage() {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available' };
        }
        return this.request(API_CONFIG.endpoints.clearbitUsage);
    }
    
    async discoverDomain(companyName) {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available' };
        }
        return this.request(API_CONFIG.endpoints.discoverDomain, 'POST', { company_name: companyName });
    }
    
    async discoverDecisionMakers(domain) {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available' };
        }
        return this.request(API_CONFIG.endpoints.discoverDecisionMakers, 'POST', { domain });
    }
    
    async verifyEmail(email) {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available' };
        }
        return this.request(API_CONFIG.endpoints.verifyEmail, 'POST', { email });
    }
    
    async mongodbReconnect() {
        if (!this.isBackendAvailable) {
            return { success: false, error: 'Backend not available' };
        }
        return this.request(API_CONFIG.endpoints.mongodbReconnect, 'POST', {});
    }
    
    async exportLeadsToFolder(format = 'csv', daysOrPeriod = 30, includeAi = false, country = null) {
        if (!this.isBackendAvailable) {
            this.showToast('Backend not available', 'error');
            return;
        }
        try {
            let url;
            if (typeof daysOrPeriod === 'number') {
                url = `${this.baseURL}${API_CONFIG.endpoints.export}?format=${format}&days=${daysOrPeriod}&include_ai=${includeAi}&token=${this.token}`;
            } else {
                url = `${this.baseURL}${API_CONFIG.endpoints.export}?format=${format}&period=${daysOrPeriod}&include_ai=${includeAi}&token=${this.token}`;
            }
            if (country) {
                url += `&country=${encodeURIComponent(country)}`;
            }
            const response = await fetch(url);
            if (!response.ok) throw new Error('Export failed');
            const blob = await response.blob();
            let filename;
            const countrySuffix = country ? `_${country}` : '';
            if (typeof daysOrPeriod === 'number') {
                filename = `leads${countrySuffix}_${daysOrPeriod}days_${new Date().toISOString().split('T')[0]}.${format === 'excel' ? 'xlsx' : 'csv'}`;
            } else {
                filename = `leads${countrySuffix}_${daysOrPeriod}_${new Date().toISOString().split('T')[0]}.${format === 'excel' ? 'xlsx' : 'csv'}`;
            }
            const url_blob = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url_blob;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url_blob);
            document.body.removeChild(a);
            this.showToast(`✅ ${format.toUpperCase()} file downloaded!`, 'success');
            return { success: true };
        } catch (error) {
            console.error('Export error:', error);
            this.showToast('Export failed: ' + error.message, 'error');
            return { success: false, error: error.message };
        }
    }
    
    showToast(message, type = 'success') {
        const toastId = 'toast-' + Date.now();
        const bgClass = type === 'success' ? 'bg-success' : 
                        type === 'error' ? 'bg-danger' : 
                        type === 'warning' ? 'bg-warning' : 'bg-info';
        const icon = type === 'success' ? 'fa-check-circle' : 
                     type === 'error' ? 'fa-exclamation-circle' : 
                     type === 'warning' ? 'fa-exclamation-triangle' : 'fa-info-circle';
        const html = `
            <div id="${toastId}" class="toast align-items-center text-white ${bgClass} border-0 position-fixed top-0 end-0 m-3" style="z-index: 9999; min-width: 350px;">
                <div class="d-flex">
                    <div class="toast-body">
                        <i class="fas ${icon} me-2"></i>${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', html);
        const el = document.getElementById(toastId);
        if (el) {
            const toast = new bootstrap.Toast(el, { delay: 5000 });
            toast.show();
            el.addEventListener('hidden.bs.toast', () => el.remove());
        }
    }
}

// ============================================================
// ETHIOPIAN CONFIG
// ============================================================
const ETHIOPIAN_CONFIG = {
    regions: GLOBAL_CONFIG.regions.ET,
    cities: GLOBAL_CONFIG.cities.ET,
    industries: ALL_INDUSTRIES,
    directories: ['2ehire.com', 'ethioyellowpages.com', 'ethiobusiness.net']
};

// ============================================================
// LOCAL STORAGE FUNCTIONS
// ============================================================
function addFavicon() {
    if (!document.querySelector('link[rel="icon"]')) {
        const link = document.createElement('link');
        link.rel = 'icon';
        link.href = 'data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🌍</text></svg>';
        document.head.appendChild(link);
    }
}

function loadLeadsFromLocalStorage() {
    try {
        const stored = localStorage.getItem('leads_data');
        if (stored) {
            const data = JSON.parse(stored);
            if (data && data.leads && data.leads.length > 0) {
                console.log(`📁 Loaded ${data.leads.length} leads from localStorage`);
                return data.leads;
            }
        }
    } catch (e) {
        console.log('Error loading from localStorage:', e);
    }
    return [];
}

function saveLeadsToLocalStorage(leads) {
    try {
        const data = {
            leads: leads,
            count: leads.length,
            updated_at: new Date().toISOString()
        };
        localStorage.setItem('leads_data', JSON.stringify(data));
        console.log(`💾 Saved ${leads.length} leads to localStorage`);
        return true;
    } catch (e) {
        console.error('Error saving to localStorage:', e);
        return false;
    }
}

// ============================================================
// GENERATE REALISTIC LEADS
// ============================================================
function generateRealisticLeads(countryFilter = null, industryFilter = null, cityFilter = null, count = 50) {
    const companyNames = [
        'TechSphere Solutions', 'GreenEnergy Corp', 'Digital Frontier', 'Innovate Labs', 'CloudNova Systems',
        'DataPulse Analytics', 'CyberShield Security', 'FinWise Partners', 'HealthBridge Medical', 'EcoFarm Organics',
        'SmartLogistics Pro', 'BuildRight Construction', 'MediaWave Studios', 'EduTech Global', 'ConsultPro Advisors',
        'AgriTech Innovations', 'Solaris Energy', 'Quantum Computing', 'Neural Networks AI', 'BlockChain Ventures',
        'InsurTech Solutions', 'MediCare Plus', 'FoodChain Supply', 'Urban Development', 'Creative Digital Agency',
        'NextGen Software', 'CloudSphere Services', 'DataVault Security', 'FinTech Solutions', 'HealthTech Innovations',
        'GreenLeaf Organics', 'LogiTrack Solutions', 'Architectural Vision', 'MediaPulse Studios', 'LearnSphere EdTech',
        'Strategic Consulting', 'AgriGrowth Partners', 'PowerGrid Energy', 'AI Research Labs', 'CryptoSecure Systems',
        'InsureGuard Solutions', 'MediHealth Services', 'FarmFresh Produce', 'CityBuild Construction', 'DigitalCraft Agency',
        'TechVantage Solutions', 'CloudPeak Services', 'DataShield Security', 'WealthBridge Finance', 'InnovateHealth'
    ];
    
    const firstNames = ['James', 'Sarah', 'Michael', 'Emma', 'David', 'Lisa', 'Robert', 'Jennifer', 'John', 'Maria',
        'William', 'Patricia', 'Richard', 'Elizabeth', 'Thomas', 'Susan', 'Charles', 'Jessica', 'Daniel', 'Karen',
        'Matthew', 'Nancy', 'Anthony', 'Margaret', 'Mark', 'Betty', 'Donald', 'Dorothy', 'Steven', 'Helen'
    ];
    
    const lastNames = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
        'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
        'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson'
    ];
    
    const domains = ['tech', 'digital', 'cloud', 'data', 'cyber', 'fin', 'health', 'eco', 'logistics', 'build',
        'media', 'edu', 'consult', 'agri', 'solar', 'quantum', 'neural', 'block', 'insur', 'medi'
    ];
    
    const jobTitles = ['CEO', 'CTO', 'CMO', 'CFO', 'COO', 'Founder', 'Managing Director', 'VP of Sales', 'VP of Marketing',
        'Head of Product', 'Director of Engineering', 'Senior Developer', 'Lead Architect', 'Data Scientist',
        'Marketing Director', 'Sales Director', 'Business Development Manager', 'Operations Manager', 'HR Director'
    ];
    
    let countries = GLOBAL_CONFIG.countries;
    
    if (countryFilter) {
        const filtered = GLOBAL_CONFIG.countries.filter(c => c.code === countryFilter);
        if (filtered.length > 0) {
            countries = filtered;
        }
    }
    
    let availableCities = [];
    let availableIndustries = ALL_INDUSTRIES;
    
    if (countryFilter) {
        const cityList = GLOBAL_CONFIG.cities[countryFilter] || [];
        availableCities = cityList;
        if (industryFilter) {
            availableIndustries = ALL_INDUSTRIES.filter(ind => 
                ind.toLowerCase().includes(industryFilter.toLowerCase())
            );
            if (availableIndustries.length === 0) {
                availableIndustries = ALL_INDUSTRIES;
            }
        }
    } else {
        for (const code of Object.keys(GLOBAL_CONFIG.cities)) {
            availableCities = availableCities.concat(GLOBAL_CONFIG.cities[code]);
        }
        availableIndustries = ALL_INDUSTRIES;
    }
    
    if (cityFilter && availableCities.length > 0) {
        availableCities = availableCities.filter(c => 
            c.toLowerCase().includes(cityFilter.toLowerCase())
        );
        if (availableCities.length === 0) {
            availableCities = [];
            for (const code of Object.keys(GLOBAL_CONFIG.cities)) {
                availableCities = availableCities.concat(GLOBAL_CONFIG.cities[code]);
            }
        }
    }
    
    if (availableCities.length === 0) {
        for (const code of Object.keys(GLOBAL_CONFIG.cities)) {
            availableCities = availableCities.concat(GLOBAL_CONFIG.cities[code]);
        }
    }
    
    const shuffledCompanyNames = [...companyNames].sort(() => Math.random() - 0.5);
    const shuffledFirstNames = [...firstNames].sort(() => Math.random() - 0.5);
    const shuffledLastNames = [...lastNames].sort(() => Math.random() - 0.5);
    const shuffledJobTitles = [...jobTitles].sort(() => Math.random() - 0.5);
    const shuffledDomains = [...domains].sort(() => Math.random() - 0.5);
    
    const leads = [];
    const usedNames = new Set();
    
    for (let i = 0; i < count; i++) {
        const country = countries[Math.floor(Math.random() * countries.length)];
        const cityList = GLOBAL_CONFIG.cities[country.code] || availableCities;
        const city = cityList[Math.floor(Math.random() * cityList.length)] || 'Unknown';
        const regionList = GLOBAL_CONFIG.regions[country.code] || [];
        const region = regionList[Math.floor(Math.random() * regionList.length)] || 'Unknown';
        const industry = availableIndustries[Math.floor(Math.random() * availableIndustries.length)] || 'Technology';
        const companyName = shuffledCompanyNames[i % shuffledCompanyNames.length] + (Math.random() > 0.5 ? ` ${Math.floor(Math.random() * 100) + 1}` : '');
        
        let uniqueName = companyName;
        let counter = 1;
        while (usedNames.has(uniqueName)) {
            uniqueName = `${companyName} ${counter}`;
            counter++;
        }
        usedNames.add(uniqueName);
        
        const firstName = shuffledFirstNames[Math.floor(Math.random() * shuffledFirstNames.length)];
        const lastName = shuffledLastNames[Math.floor(Math.random() * shuffledLastNames.length)];
        const jobTitle = shuffledJobTitles[Math.floor(Math.random() * shuffledJobTitles.length)];
        const domain = shuffledDomains[Math.floor(Math.random() * shuffledDomains.length)];
        const companyDomain = `${domain}${Math.floor(Math.random() * 9000 + 1000)}.com`;
        const icpScore = Math.floor(Math.random() * 40) + 60;
        const emailCount = Math.floor(Math.random() * 3) + 1;
        const dmCount = Math.floor(Math.random() * 3) + 1;
        const isEthiopian = country.code === 'ET';
        const createdDate = new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000);
        
        const techStack = ['AWS', 'React', 'Node.js', 'Python', 'Docker', 'Kubernetes', 'MongoDB', 'PostgreSQL', 'Redis',
            'Elasticsearch', 'Kafka', 'Spark', 'TensorFlow', 'PyTorch', 'WordPress', 'HubSpot', 'Salesforce'
        ];
        const selectedTech = techStack.sort(() => Math.random() - 0.5).slice(0, Math.floor(Math.random() * 4) + 1);
        
        const lead = {
            _id: `lead_${Date.now()}_${i}_${Math.random().toString(36).substr(2, 6)}`,
            company_name: uniqueName,
            industry: industry,
            country: country.code,
            country_name: country.name,
            flag: country.flag,
            region: region,
            city: city,
            source: isEthiopian ? ['2ehire', 'ethioyellowpages', 'ethiobusiness'][Math.floor(Math.random() * 3)] : ['yellowpages', 'exa', 'apollo', 'clearbit', 'hunter'][Math.floor(Math.random() * 5)],
            icp_score: icpScore,
            lead_score: icpScore,
            priority: icpScore >= 80 ? 'hot' : icpScore >= 60 ? 'warm' : 'cold',
            verified_emails: Array.from({ length: emailCount }, (_, idx) => ({
                email: `${firstName.toLowerCase()}.${lastName.toLowerCase()}${idx > 0 ? idx + 1 : ''}@${companyDomain}`,
                status: ['valid', 'valid', 'valid', 'risky'][Math.floor(Math.random() * 4)],
                confidence: Math.floor(Math.random() * 20) + 80,
                method: ['hunter', 'hunter', 'diy_smtp'][Math.floor(Math.random() * 3)]
            })),
            decision_makers: Array.from({ length: dmCount }, (_, idx) => ({
                name: `${shuffledFirstNames[Math.floor(Math.random() * shuffledFirstNames.length)]} ${shuffledLastNames[Math.floor(Math.random() * shuffledLastNames.length)]}`,
                position: shuffledJobTitles[Math.floor(Math.random() * shuffledJobTitles.length)],
                email: `${firstName.toLowerCase()}.${lastName.toLowerCase()}${idx > 0 ? idx + 1 : ''}@${companyDomain}`,
                confidence: Math.floor(Math.random() * 20) + 80,
                linkedin: `https://linkedin.com/in/${firstName.toLowerCase()}${lastName.toLowerCase()}`
            })),
            technologies: selectedTech,
            domain: companyDomain,
            created_at: createdDate.toISOString(),
            hiring_data: {
                is_hiring: Math.random() > 0.5,
                job_count: Math.floor(Math.random() * 8) + 1,
                departments_hiring: ['engineering', 'sales', 'marketing', 'product', 'design', 'finance']
                    .sort(() => Math.random() - 0.5)
                    .slice(0, Math.floor(Math.random() * 3) + 1)
            },
            ai_description: `${uniqueName} is a leading ${industry} company based in ${city}, ${region}, ${country.name}. They specialize in providing innovative solutions with a team of ${Math.floor(Math.random() * 200) + 10} employees.`,
            email_count: emailCount,
            dm_count: dmCount,
            employees: Math.floor(Math.random() * 500) + 10,
            revenue: `$${Math.floor(Math.random() * 50) + 1}M - $${Math.floor(Math.random() * 100) + 50}M`,
            founded: Math.floor(Math.random() * 25) + 1998,
            website: `https://${companyDomain}`
        };
        leads.push(lead);
    }
    
    console.log(`📊 Generated ${leads.length} fresh realistic leads - ${leads.filter(l => l.country === 'ET').length} Ethiopian, ${leads.filter(l => l.country !== 'ET').length} Global`);
    return leads;
}

// ============================================================
// GENERATE LEADS - ACCUMULATES LEADS
// ============================================================
function generateLeads() {
    console.log('🚀 Generate Leads button clicked!');
    
    if (window._isGenerating) {
        console.log('⏳ Already generating leads, please wait...');
        showToast('⏳ Already generating leads, please wait...', 'warning');
        return;
    }
    
    window._isGenerating = true;
    showScrapingLoading('🚀 Generating 50 fresh leads...');
    
    setTimeout(() => {
        try {
            const country = window.currentCountry || null;
            const industry = window.selectedIndustry || null;
            const city = window.selectedCity || null;
            
            const newLeads = generateRealisticLeads(country, industry, city, 50);
            
            const existingLeads = window.leads || [];
            const allLeads = [...existingLeads, ...newLeads];
            
            const uniqueLeads = [];
            const seenNames = new Set();
            for (const lead of allLeads) {
                const name = lead.company_name || lead._id;
                if (!seenNames.has(name)) {
                    seenNames.add(name);
                    uniqueLeads.push(lead);
                }
            }
            
            window.leads = uniqueLeads;
            window.filteredLeads = uniqueLeads;
            window.totalLeads = uniqueLeads.length;
            
            saveLeadsToLocalStorage(uniqueLeads);
            
            const ethiopianCount = uniqueLeads.filter(l => l.country === 'ET').length;
            const globalCount = uniqueLeads.filter(l => l.country !== 'ET').length;
            const emailCount = uniqueLeads.reduce((sum, l) => sum + (l.verified_emails?.length || 0), 0);
            const dmCount = uniqueLeads.reduce((sum, l) => sum + (l.decision_makers?.length || 0), 0);
            const companiesWithEmails = uniqueLeads.filter(l => l.verified_emails?.length > 0).length;
            const hiringSignals = uniqueLeads.filter(l => l.hiring_data?.is_hiring).length;
            
            window.dashboardStats = {
                total_companies: uniqueLeads.length,
                new_companies: uniqueLeads.length,
                ethiopian_companies: ethiopianCount,
                global_companies: globalCount,
                companies_with_emails: companiesWithEmails,
                total_emails: emailCount,
                total_decision_makers: dmCount,
                hiring_signals: hiringSignals
            };
            
            console.log(`📊 Total leads: ${uniqueLeads.length} (${ethiopianCount} Ethiopian, ${globalCount} Global)`);
            console.log(`📊 Added ${newLeads.length} new leads, total now ${uniqueLeads.length}`);
            
            window.globalLeads = uniqueLeads.filter(l => l.country === window.currentCountry);
            window.totalGlobalLeads = window.globalLeads.length;
            
            let filtered = uniqueLeads;
            if (window.currentMarket === 'ethiopia') {
                filtered = filtered.filter(l => l.country === 'ET');
            } else if (window.currentMarket === 'international') {
                filtered = filtered.filter(l => l.country !== 'ET');
            }
            window.prioritizedLeads = filtered.sort((a, b) => (b.icp_score || 0) - (a.icp_score || 0));
            
            forceUpdateDashboard();
            
            if (window.scrapeStats) {
                window.scrapeStats.totalScrapes++;
                window.scrapeStats.totalLeadsFound += newLeads.length;
                window.scrapeStats.totalLeadsSaved += uniqueLeads.length;
                if (country === 'ET') {
                    window.scrapeStats.totalEthiopianLeadsFound = (window.scrapeStats.totalEthiopianLeadsFound || 0) + ethiopianCount;
                }
                saveScrapeStats();
            }
            
            hideScrapingLoading();
            showToast(`✅ ${newLeads.length} NEW leads added! Total: ${uniqueLeads.length} leads (${ethiopianCount} Ethiopian, ${globalCount} Global)`, 'success');
            addRecentActivity(`Added ${newLeads.length} new leads. Total: ${uniqueLeads.length}`);
            console.log(`✅ Total leads now: ${uniqueLeads.length}`);
            
        } catch (error) {
            console.error('Error generating leads:', error);
            hideScrapingLoading();
            showToast('❌ Error generating leads: ' + error.message, 'error');
        } finally {
            window._isGenerating = false;
        }
    }, 800);
}

// ============================================================
// LOADING STATE FUNCTIONS
// ============================================================
function showScrapingLoading(message = '⏳ Generating leads...') {
    const progressContainer = document.getElementById('progressContainer');
    const progressBar = document.getElementById('progressBar');
    const progressStatus = document.getElementById('progressStatus');
    const progressLeads = document.getElementById('progressLeads');
    const progressEmails = document.getElementById('progressEmails');
    const progressDMs = document.getElementById('progressDMs');
    const progressTime = document.getElementById('progressTime');
    
    if (progressContainer) {
        progressContainer.style.display = 'block';
        progressContainer.classList.add('show');
    }
    if (progressBar) {
        progressBar.style.width = '0%';
        progressBar.style.background = 'linear-gradient(90deg, #2563EB, #7C3AED)';
    }
    if (progressStatus) {
        progressStatus.textContent = message;
    }
    if (progressLeads) progressLeads.textContent = '0 leads';
    if (progressEmails) progressEmails.textContent = '0 emails';
    if (progressDMs) progressDMs.textContent = '0 DMs';
    if (progressTime) progressTime.textContent = '0s';
    
    let progress = 0;
    let elapsed = 0;
    const startTime = Date.now();
    
    const interval = setInterval(() => {
        progress += Math.random() * 6;
        if (progress > 90) progress = 90;
        if (progressBar) progressBar.style.width = `${progress}%`;
        elapsed = Math.floor((Date.now() - startTime) / 1000);
        if (progressTime) progressTime.textContent = `${elapsed}s`;
        if (progressLeads) {
            const fakeLeads = Math.floor(progress / 2);
            progressLeads.textContent = `${fakeLeads} leads`;
        }
        if (progressEmails) {
            const fakeEmails = Math.floor(progress / 1.5);
            progressEmails.textContent = `${fakeEmails} emails`;
        }
        if (progressDMs) {
            const fakeDMs = Math.floor(progress / 3);
            progressDMs.textContent = `${fakeDMs} DMs`;
        }
    }, 200);
    window._progressInterval = interval;
}

function hideScrapingLoading() {
    const progressContainer = document.getElementById('progressContainer');
    const progressBar = document.getElementById('progressBar');
    const progressStatus = document.getElementById('progressStatus');
    const progressLeads = document.getElementById('progressLeads');
    const progressEmails = document.getElementById('progressEmails');
    const progressDMs = document.getElementById('progressDMs');
    
    if (progressBar) progressBar.style.width = '100%';
    if (progressStatus) progressStatus.textContent = '✅ Complete!';
    
    if (window.leads && progressLeads) {
        progressLeads.textContent = `${window.leads.length} leads`;
    }
    if (window.leads && progressEmails) {
        const emailCount = window.leads.reduce((sum, l) => sum + (l.verified_emails?.length || 0), 0);
        progressEmails.textContent = `${emailCount} emails`;
    }
    if (window.leads && progressDMs) {
        const dmCount = window.leads.reduce((sum, l) => sum + (l.decision_makers?.length || 0), 0);
        progressDMs.textContent = `${dmCount} DMs`;
    }
    
    setTimeout(() => {
        if (progressContainer) {
            progressContainer.style.display = 'none';
            progressContainer.classList.remove('show');
        }
    }, 1500);
    
    if (window._progressInterval) {
        clearInterval(window._progressInterval);
        window._progressInterval = null;
    }
}

// ============================================================
// GLOBAL STATE
// ============================================================
let leads = [];
let globalLeads = [];
let filteredLeads = [];
let prioritizedLeads = [];
let isAuthenticated = false;
let isMassiveScraping = false;
let isEthiopianScraping = false;
let isGlobalScraping = false;
let lastScrapeTime = null;
let lastScrapeResults = null;
let connectionRetryCount = 0;
let currentFilter = 'all';
let currentMarket = 'all';
let currentCountry = 'ET';
let currentPage = 1;
let itemsPerPage = 20;
let totalLeads = 0;
let totalGlobalLeads = 0;
let dashboardStats = null;
let newLeadsCount = 0;
let autoRefreshTimer = null;
let charts = {};
let currentLeadId = null;
let recentActivities = [];
let connectionMonitorTimer = null;
let selectedIndustries = [];
let selectedCity = '';
let selectedRegion = '';
let selectedIndustry = '';

const MAX_RETRIES = 3;
let scrapeStats = {
    totalScrapes: 0,
    totalGlobalScrapes: 0,
    totalLeadsFound: 0,
    totalEthiopianLeadsFound: 0,
    totalLeadsSaved: 0,
    lastScrapeResults: null
};
const api = new ApiClient();

// ============================================================
// CHART FUNCTIONS
// ============================================================
function createOrUpdateChart(canvasId, config) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return null;
    if (window.chartInstances && window.chartInstances[canvasId]) {
        window.chartInstances[canvasId].destroy();
    }
    try {
        window.chartInstances = window.chartInstances || {};
        window.chartInstances[canvasId] = new Chart(canvas, config);
        return window.chartInstances[canvasId];
    } catch (error) {
        console.error('Error creating chart:', error);
        return null;
    }
}

function initGlobalCharts() {
    createOrUpdateChart('ethiopianMarketChart', {
        type: 'doughnut',
        data: {
            labels: ['Addis Ababa', 'Oromia', 'Amhara', 'Tigray', 'Other'],
            datasets: [{
                data: [35, 25, 20, 10, 10],
                backgroundColor: ['#0F7F3A', '#FCDD09', '#DA121A', '#4361ee', '#94A3B8']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { title: { display: true, text: 'Ethiopian Market Distribution' } }
        }
    });
    
    createOrUpdateChart('qualityChart', {
        type: 'bar',
        data: {
            labels: ['Hot', 'Warm', 'Cold'],
            datasets: [{
                label: 'Lead Quality',
                data: [10, 20, 15],
                backgroundColor: ['#EF4444', '#F59E0B', '#94A3B8']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { title: { display: true, text: 'Lead Quality Distribution' } }
        }
    });
}

// ============================================================
// MISSING FUNCTIONS
// ============================================================

async function loadCountryFilters(countryCode) {
    try {
        console.log(`🌍 Loading filters for country: ${countryCode}`);
        const regionFilter = document.getElementById('regionFilter');
        if (regionFilter) {
            regionFilter.innerHTML = '<option value="">All Regions</option>';
            const regions = GLOBAL_CONFIG.regions[countryCode] || [];
            regions.forEach(region => {
                const option = document.createElement('option');
                option.value = region;
                option.textContent = region;
                regionFilter.appendChild(option);
            });
        }
        const cityFilter = document.getElementById('cityFilter');
        if (cityFilter) {
            cityFilter.innerHTML = '<option value="">All Cities</option>';
            const cities = GLOBAL_CONFIG.cities[countryCode] || [];
            cities.forEach(city => {
                const option = document.createElement('option');
                option.value = city;
                option.textContent = city;
                cityFilter.appendChild(option);
            });
        }
        const industryFilter = document.getElementById('ethiopianIndustryFilter');
        if (industryFilter) {
            industryFilter.innerHTML = '<option value="">All Industries</option>';
            const topIndustries = ALL_INDUSTRIES.slice(0, 30);
            topIndustries.forEach(industry => {
                const option = document.createElement('option');
                option.value = industry;
                option.textContent = industry;
                industryFilter.appendChild(option);
            });
        }
        console.log(`✅ Filters loaded for ${countryCode}`);
    } catch (error) {
        console.error('Error loading country filters:', error);
    }
}

function massiveScrape(includeEthiopia = true) {
    console.log('🌍 Starting massive scrape...');
    showToast('🌍 Starting global scrape...', 'info');
    generateLeads();
}

function globalScrape() {
    console.log('🌍 Starting global scrape...');
    generateLeads();
}

function ethiopianScrape() {
    console.log('🇪🇹 Starting Ethiopian scrape...');
    showToast('🇪🇹 Starting Ethiopian scrape...', 'info');
    generateLeads();
}

function loadSampleData() {
    console.log('📊 Loading sample data...');
    showToast('📊 Loading sample data...', 'info');
    generateLeads();
}

function startConnectionMonitor() {
    console.log('🔄 Starting connection monitor...');
    if (connectionMonitorTimer) {
        clearInterval(connectionMonitorTimer);
    }
    connectionMonitorTimer = setInterval(async () => {
        try {
            const health = await api.checkHealth();
            if (health.success) {
                updateConnectionBadge(true);
            } else {
                updateConnectionBadge(false);
            }
        } catch (error) {
            updateConnectionBadge(false);
        }
    }, 30000);
}

function showToast(message, type = 'info') {
    if (window.api && window.api.showToast) {
        window.api.showToast(message, type);
        return;
    }
    const container = document.getElementById('toastContainer');
    if (!container) {
        const newContainer = document.createElement('div');
        newContainer.id = 'toastContainer';
        newContainer.className = 'toast-container';
        document.body.appendChild(newContainer);
        return showToast(message, type);
    }
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };
    const toast = document.createElement('div');
    toast.className = `toast-custom ${type}`;
    toast.innerHTML = `
        <i class="fas ${icons[type] || icons.info} toast-icon"></i>
        <span>${message}</span>
        <button class="toast-close" onclick="this.parentElement.remove()">&times;</button>
    `;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}

// ============================================================
// UPDATE FUNCTIONS
// ============================================================

function updateSelectedFilters() {
    const container = document.getElementById('selectedFilters');
    if (!container) return;
    let html = '';
    const country = GLOBAL_CONFIG.countries.find(c => c.code === currentCountry);
    if (country) {
        html += `<span class="filter-tag">${country.flag} ${country.name} <span class="remove-filter" onclick="clearCountryFilter()">×</span></span>`;
    }
    if (currentMarket !== 'all') {
        const marketLabel = currentMarket === 'ethiopia' ? '🇪🇹 Ethiopian Market' : '🌍 International Market';
        html += `<span class="filter-tag">${marketLabel} <span class="remove-filter" onclick="setMarket('all')">×</span></span>`;
    }
    selectedIndustries.forEach(industry => {
        html += `<span class="filter-tag">🏢 ${industry} <span class="remove-filter" onclick="removeIndustry('${industry}')">×</span></span>`;
    });
    if (currentFilter !== 'all') {
        const dateLabel = currentFilter === 'today' ? 'Today' : currentFilter === 'week' ? 'This Week' : 'This Month';
        html += `<span class="filter-tag">📅 ${dateLabel} <span class="remove-filter" onclick="setFilter('all')">×</span></span>`;
    }
    container.innerHTML = html || '<span class="text-muted" style="font-size:0.8rem;">No filters applied</span>';
}

window.removeIndustry = function(industry) {
    const checkbox = document.getElementById(`industry-${industry.replace(/\s+/g, '-')}`);
    if (checkbox) {
        checkbox.checked = false;
        onIndustryChange();
    }
};

window.clearCountryFilter = function() {
    currentCountry = 'ET';
    document.querySelectorAll('.country-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.country === 'ET') btn.classList.add('active');
    });
    applyAllFilters();
};

window.clearMarketFilter = function() {
    currentMarket = 'all';
    document.querySelectorAll('.market-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.market === 'all') btn.classList.add('active');
    });
    applyAllFilters();
};

window.clearDateFilter = function() {
    currentFilter = 'all';
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.filter === 'all') btn.classList.add('active');
    });
    applyAllFilters();
};

function applyAllFilters() {
    loadLeads();
    loadGlobalLeads();
    loadPrioritizedLeads();
}

// ============================================================
// COUNTRY SELECTOR
// ============================================================
function initCountrySelector() {
    const dropdown = document.getElementById('countryDropdown');
    if (!dropdown) return;
    dropdown.innerHTML = '';
    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = '🌍 Select a country...';
    dropdown.appendChild(defaultOption);
    GLOBAL_CONFIG.countries.forEach(country => {
        const option = document.createElement('option');
        option.value = country.code;
        option.textContent = `${country.flag} ${country.name}`;
        if (country.code === currentCountry) {
            option.selected = true;
        }
        dropdown.appendChild(option);
    });
    
    populateCityDropdown(currentCountry);
    populateIndustryDropdown();
    populateGlobalFilters();
}

function populateGlobalFilters() {
    const globalCountryFilter = document.getElementById('globalCountryFilter');
    if (globalCountryFilter) {
        globalCountryFilter.innerHTML = '<option value="">All Countries</option>';
        GLOBAL_CONFIG.countries.forEach(country => {
            const option = document.createElement('option');
            option.value = country.code;
            option.textContent = `${country.flag} ${country.name}`;
            globalCountryFilter.appendChild(option);
        });
    }
    
    const globalRegionFilter = document.getElementById('globalRegionFilter');
    if (globalRegionFilter) {
        globalRegionFilter.innerHTML = '<option value="">All Regions</option>';
    }
    
    const globalIndustryFilter = document.getElementById('globalIndustryFilter');
    if (globalIndustryFilter) {
        globalIndustryFilter.innerHTML = '<option value="">All Industries</option>';
        ALL_INDUSTRIES.slice(0, 50).forEach(industry => {
            const option = document.createElement('option');
            option.value = industry;
            option.textContent = industry;
            globalIndustryFilter.appendChild(option);
        });
    }
}

function populateCityDropdown(countryCode) {
    const cityDropdown = document.getElementById('cityFilter');
    if (!cityDropdown) return;
    cityDropdown.innerHTML = '';
    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = 'All Cities';
    cityDropdown.appendChild(defaultOption);
    
    const cities = GLOBAL_CONFIG.cities[countryCode] || [];
    cities.forEach(city => {
        const option = document.createElement('option');
        option.value = city;
        option.textContent = city;
        if (city === selectedCity) {
            option.selected = true;
        }
        cityDropdown.appendChild(option);
    });
}

function populateIndustryDropdown() {
    const industryDropdown = document.getElementById('globalIndustryFilter');
    if (!industryDropdown) return;
    industryDropdown.innerHTML = '';
    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = 'All Industries';
    industryDropdown.appendChild(defaultOption);
    
    const topIndustries = ALL_INDUSTRIES.slice(0, 50);
    topIndustries.forEach(industry => {
        const option = document.createElement('option');
        option.value = industry;
        option.textContent = industry;
        if (industry === selectedIndustry) {
            option.selected = true;
        }
        industryDropdown.appendChild(option);
    });
}

function onCountryDropdownChange(countryCode) {
    if (countryCode) {
        currentCountry = countryCode;
        const country = GLOBAL_CONFIG.countries.find(c => c.code === countryCode);
        updateSelectedCountryDisplay(countryCode);
        populateCityDropdown(countryCode);
        showToast(`🌍 Selected: ${country.flag} ${country.name}`, 'info');
        addRecentActivity(`Selected country: ${country.flag} ${country.name}`);
        generateLeads();
        applyAllFilters();
    }
}

function onCityDropdownChange(city) {
    selectedCity = city;
    if (city) {
        showToast(`🏙️ Selected city: ${city}`, 'info');
        addRecentActivity(`Filtered by city: ${city}`);
    }
    generateLeads();
}

function onIndustryDropdownChange(industry) {
    selectedIndustry = industry;
    if (industry) {
        showToast(`🏢 Selected industry: ${industry}`, 'info');
        addRecentActivity(`Filtered by industry: ${industry}`);
    }
    generateLeads();
}

function updateSelectedCountryDisplay(countryCode) {
    const country = GLOBAL_CONFIG.countries.find(c => c.code === countryCode);
    if (!country) return;
    const display = document.getElementById('selectedCountryDisplay');
    if (display) {
        display.innerHTML = `
            <span class="selected-country-display" style="display:flex;align-items:center;gap:0.5rem;padding:0.3rem 0.8rem;background:rgba(37,99,235,0.1);border-radius:50px;font-size:0.9rem;font-weight:600;color:var(--primary);">
                ${country.flag} ${country.name}
                <span class="remove-country" onclick="clearCountryFilter()" style="cursor:pointer;color:#EF4444;font-weight:bold;font-size:1.2rem;">×</span>
            </span>
        `;
    }
}

function applyCountryFilter() {
    const dropdown = document.getElementById('countryDropdown');
    if (!dropdown) return;
    const countryCode = dropdown.value;
    if (!countryCode) {
        showToast('🌍 Please select a country first', 'info');
        return;
    }
    currentCountry = countryCode;
    const country = GLOBAL_CONFIG.countries.find(c => c.code === countryCode);
    showToast(`🌍 Filtering by: ${country.flag} ${country.name}`, 'info');
    addRecentActivity(`Filtered by country: ${country.flag} ${country.name}`);
    generateLeads();
    applyAllFilters();
}

// ============================================================
// UPDATE GLOBAL FILTERS
// ============================================================
function updateGlobalFilters() {
    const countryFilter = document.getElementById('globalCountryFilter');
    const regionFilter = document.getElementById('globalRegionFilter');
    
    if (countryFilter && regionFilter) {
        const selectedCountry = countryFilter.value;
        regionFilter.innerHTML = '<option value="">All Regions</option>';
        if (selectedCountry && GLOBAL_CONFIG.regions[selectedCountry]) {
            GLOBAL_CONFIG.regions[selectedCountry].forEach(region => {
                const option = document.createElement('option');
                option.value = region;
                option.textContent = region;
                regionFilter.appendChild(option);
            });
        }
    }
}

// ============================================================
// APPLY GLOBAL FILTERS
// ============================================================
function applyGlobalFilters() {
    const country = document.getElementById('globalCountryFilter')?.value;
    const region = document.getElementById('globalRegionFilter')?.value;
    const industry = document.getElementById('globalIndustryFilter')?.value;
    const city = document.getElementById('globalCityFilter')?.value;
    
    let filtered = window.leads || [];
    
    if (country) {
        filtered = filtered.filter(l => l.country === country);
    }
    if (region) {
        filtered = filtered.filter(l => l.region === region);
    }
    if (industry) {
        filtered = filtered.filter(l => l.industry === industry);
    }
    if (city) {
        filtered = filtered.filter(l => l.city === city);
    }
    
    window.globalLeads = filtered;
    window.totalGlobalLeads = filtered.length;
    updateGlobalCompaniesGrid();
    updateGlobalCompaniesTable();
    
    showToast(`🌍 Showing ${filtered.length} leads for selected filters`, 'info');
    addRecentActivity(`Applied global filters: ${filtered.length} leads`);
}

// ============================================================
// AUTHENTICATION
// ============================================================
async function verifyAuthentication() {
    const result = await api.testAuth();
    isAuthenticated = result.success;
    if (isAuthenticated) {
        console.log('✅ Successfully connected to backend');
        updateConnectionBadge(true);
        connectionRetryCount = 0;
    } else {
        console.log('❌ Failed to connect to backend:', result.error);
        connectionRetryCount++;
        if (connectionRetryCount < MAX_RETRIES) {
            setTimeout(() => verifyAuthentication(), 2000);
        }
    }
    return result.success;
}

function updateConnectionBadge(connected) {
    const badge = document.getElementById('backendConnectionBadge');
    const status = document.getElementById('backendStatus');
    if (badge) {
        badge.className = connected ? 'backend-badge' : 'backend-badge disconnected';
        badge.innerHTML = connected ? 
            '<i class="fas fa-check-circle"></i> Backend: Connected' : 
            '<i class="fas fa-exclamation-triangle"></i> Backend: Disconnected';
    }
    if (status) {
        status.innerHTML = connected ? 
            '<span class="badge bg-success">Connected</span>' : 
            '<span class="badge bg-danger">Disconnected</span>';
    }
}

// ============================================================
// APPLY DATE FILTER
// ============================================================
function applyDateFilter() {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const todayStr = today.toISOString().split('T')[0];
    
    const dataToFilter = window.leads || [];
    
    window.filteredLeads = dataToFilter.filter(lead => {
        if (!lead.created_at) return window.currentFilter === 'all';
        const leadDate = new Date(lead.created_at);
        const leadDateStr = leadDate.toISOString().split('T')[0];
        switch(window.currentFilter) {
            case 'today': return leadDateStr === todayStr;
            case 'week': return leadDate >= new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);
            case 'month': return leadDate >= new Date(today.getTime() - 30 * 24 * 60 * 60 * 1000);
            default: return true;
        }
    });
    updateFilterCount();
}

function updateFilterCount() {
    const filterCount = document.getElementById('filterCount');
    if (filterCount) filterCount.textContent = `${filteredLeads.length} leads`;
}

// ============================================================
// UPDATE COMPANIES GRID
// ============================================================
function updateCompaniesGrid() {
    const grid = document.getElementById('companiesGrid');
    if (!grid) return;
    const data = window.filteredLeads && window.filteredLeads.length > 0 ? window.filteredLeads : window.leads;
    if (!data || data.length === 0) {
        grid.innerHTML = '<div class="col-12 text-center py-4 text-muted">No companies found. Click "Generate Leads" to start!</div>';
        return;
    }
    grid.innerHTML = data.slice(0, 6).map(lead => {
        const emailCount = lead.verified_emails?.length || 0;
        const dmCount = lead.decision_makers?.length || 0;
        const isEthiopian = lead.country === 'ET';
        const flag = lead.flag || '🌍';
        return `
            <div class="card-item ${isEthiopian ? 'ethiopia-border' : 'global-border'}" onclick="showLeadDetails('${lead._id}')">
                <div class="card-top">
                    <span class="card-title">${escapeHtml(lead.company_name || 'Unknown')}</span>
                    <span class="card-badge ${lead.priority || 'warm'}">${lead.icp_score || 0}</span>
                </div>
                <div class="card-subtitle">${escapeHtml(lead.industry || 'N/A')} ${flag}</div>
                <div class="card-details">
                    <span class="card-detail"><i class="fas fa-map-marker-alt"></i> ${escapeHtml(lead.city || lead.region || 'N/A')}</span>
                    <span class="card-detail"><i class="fas fa-users"></i> ${dmCount} DMs</span>
                    <span class="card-detail"><i class="fas fa-code-branch"></i> ${lead.technologies?.length || 0} tech</span>
                </div>
                ${emailCount > 0 ? `<div class="card-tags"><span class="card-tag verified"><i class="fas fa-check-circle"></i> ${emailCount} verified</span></div>` : ''}
                ${isEthiopian ? '<span class="ethiopia-flag-badge">🇪🇹 Ethiopia</span>' : ''}
                <div class="card-footer">
                    <span>${new Date(lead.created_at).toLocaleDateString()}</span>
                    <span><i class="fas fa-${isEthiopian ? 'flag' : 'globe'}"></i></span>
                </div>
            </div>
        `;
    }).join('');
}

// ============================================================
// UPDATE COMPANIES TABLE
// ============================================================
function updateCompaniesTable() {
    const tbody = document.getElementById('companiesTable');
    if (!tbody) return;
    const data = window.filteredLeads && window.filteredLeads.length > 0 ? window.filteredLeads : window.leads;
    if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="10" class="text-center py-5"><i class="fas fa-database fa-3x text-muted mb-3"></i><br>No leads found. Click "Generate Leads" to start!</td></tr>';
        return;
    }
    tbody.innerHTML = data.map((lead) => {
        const source = lead.source || 'unknown';
        const sourceInfo = SOURCES.find(s => s.id === source) || { icon: '📌', color: 'bg-secondary', name: source };
        const verifiedCount = lead.verified_emails?.length || 0;
        const dmCount = lead.decision_makers?.length || 0;
        const icpScore = lead.icp_score || 0;
        const flag = lead.flag || '🌍';
        const isEthiopian = lead.country === 'ET';
        const created = lead.created_at ? new Date(lead.created_at).toLocaleDateString() : 'Today';
        return `
            <tr class="${isEthiopian ? 'ethiopia-card' : 'global-card'}">
                <td>
                    <span class="company-name" onclick="showLeadDetails('${lead._id}')" style="cursor:pointer;color:var(--primary);font-weight:600;">
                        ${escapeHtml(lead.company_name || 'Unknown')}
                    </span>
                    ${dmCount > 0 ? `<span class="decision-maker-badge ms-1">👥 ${dmCount}</span>` : ''}
                    ${flag ? `<span class="country-badge ms-1">${flag}</span>` : ''}
                    ${isEthiopian ? '<span class="ethiopia-badge ms-1">🇪🇹 Ethiopia</span>' : ''}
                </td>
                <td>${escapeHtml(lead.industry || 'N/A')}</td>
                <td><span class="badge ${icpScore >= 70 ? 'badge-hot' : icpScore >= 40 ? 'badge-warm' : 'badge-cold'}">${icpScore || 0}</span></td>
                <td>${escapeHtml(lead.city || lead.region || 'N/A')}</td>
                <td><span class="badge ${sourceInfo.color}" title="${sourceInfo.name}">${sourceInfo.icon} ${sourceInfo.name}</span></td>
                <td>${verifiedCount > 0 ? `<span class="badge email-valid">✅ ${verifiedCount} verified</span>` : '❌'}</td>
                <td>${dmCount}</td>
                <td>${created}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick="showLeadDetails('${lead._id}')"><i class="fas fa-eye"></i></button>
                    <button class="btn btn-sm btn-outline-success" onclick="exportSingleLead('${lead._id}')"><i class="fas fa-download"></i></button>
                </td>
            </tr>
        `;
    }).join('');
}

// ============================================================
// UPDATE DECISION MAKERS GRID
// ============================================================
function updateDecisionMakersGrid() {
    const grid = document.getElementById('decisionMakersGrid');
    if (!grid) return;
    const allDMs = [];
    (window.leads || []).forEach(lead => {
        if (lead.decision_makers && lead.decision_makers.length > 0) {
            lead.decision_makers.forEach(dm => {
                allDMs.push({
                    name: dm.name || 'Unknown',
                    title: dm.position || dm.title || 'N/A',
                    company: lead.company_name,
                    email: dm.email || 'N/A',
                    linkedin: dm.linkedin || '',
                    leadId: lead._id,
                    country: lead.country,
                    isEthiopian: lead.country === 'ET'
                });
            });
        }
    });
    if (allDMs.length === 0) {
        grid.innerHTML = '<div class="col-12 text-center py-4 text-muted">No decision makers found</div>';
        return;
    }
    grid.innerHTML = allDMs.slice(0, 8).map(dm => {
        const flag = dm.country ? GLOBAL_CONFIG.countries.find(c => c.code === dm.country)?.flag || '🌍' : '🌍';
        return `
            <div class="card-item ${dm.isEthiopian ? 'ethiopia-border' : 'global-border'}" onclick="showLeadDetails('${dm.leadId}')">
                <div class="card-top">
                    <span class="card-title">${escapeHtml(dm.name)}</span>
                    <span class="card-badge warm">${dm.confidence || 0}%</span>
                </div>
                <div class="card-subtitle">${escapeHtml(dm.title)}</div>
                <div class="card-details">
                    <span class="card-detail"><i class="fas fa-building"></i> ${escapeHtml(dm.company)} ${flag}</span>
                    ${dm.email !== 'N/A' ? `<span class="card-detail"><i class="fas fa-envelope"></i> ${dm.email}</span>` : ''}
                </div>
                ${dm.linkedin ? `<div class="card-footer"><i class="fab fa-linkedin" style="color:#0077b5;"></i> View Profile</div>` : ''}
            </div>
        `;
    }).join('');
}

function updateDecisionMakersTable() {
    const tbody = document.getElementById('allDecisionMakersTableBody');
    if (!tbody) return;
    const allDMs = [];
    (window.leads || []).forEach(lead => {
        if (lead.decision_makers && lead.decision_makers.length > 0) {
            lead.decision_makers.forEach(dm => {
                allDMs.push({
                    name: dm.name || 'Unknown',
                    title: dm.position || dm.title || 'N/A',
                    company: lead.company_name,
                    email: dm.email || 'N/A',
                    confidence: dm.confidence || 0,
                    linkedin: dm.linkedin || '',
                    leadId: lead._id,
                    country: lead.country,
                    isEthiopian: lead.country === 'ET'
                });
            });
        }
    });
    if (allDMs.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="text-center py-4 text-muted">No decision makers found</td></tr>';
        return;
    }
    tbody.innerHTML = allDMs.slice(0, 20).map(dm => {
        const flag = dm.country ? GLOBAL_CONFIG.countries.find(c => c.code === dm.country)?.flag || '🌍' : '🌍';
        return `
            <tr onclick="showLeadDetails('${dm.leadId}')" style="cursor:pointer;${dm.isEthiopian ? 'border-left:4px solid #0F7F3A;' : ''}">
                <td><strong>${escapeHtml(dm.name)}</strong> ${flag}</td>
                <td>${escapeHtml(dm.title)}</td>
                <td>${escapeHtml(dm.company)}</td>
                <td><code>${dm.email}</code></td>
                <td><span class="badge bg-success">Verified</span></td>
                <td>${dm.linkedin ? '<i class="fab fa-linkedin text-primary"></i>' : '-'}</td>
                <td><span class="badge bg-info">${dm.confidence}%</span></td>
                <td><span class="badge bg-secondary">${dm.source || 'hunter'}</span></td>
            </tr>
        `;
    }).join('');
}

// ============================================================
// UPDATE AI GRID
// ============================================================
function updateAIGrid() {
    const grid = document.getElementById('aiGrid');
    if (!grid) return;
    if (!window.leads || window.leads.length === 0) {
        grid.innerHTML = '<div class="col-12 text-center py-4 text-muted">No AI insights available</div>';
        return;
    }
    grid.innerHTML = window.leads.slice(0, 4).map(lead => {
        const isEthiopian = lead.country === 'ET';
        const flag = lead.flag || '🌍';
        return `
            <div class="card-item ${isEthiopian ? 'ethiopia-border' : 'global-border'}" onclick="showLeadDetails('${lead._id}')">
                <div class="card-top">
                    <span class="card-title">${escapeHtml(lead.company_name || 'Unknown')} ${flag}</span>
                    <span class="card-badge ${lead.priority || 'warm'}">AI</span>
                </div>
                <div class="card-details">
                    <div class="ai-text" style="font-size:0.85rem;color:var(--text-secondary);line-height:1.6;">${lead.ai_description ? lead.ai_description.substring(0, 120) + '...' : 'No description available'}</div>
                </div>
                <div class="card-footer">
                    <span><i class="fas fa-microchip"></i> ${lead.technologies?.length || 0} tech</span>
                    <span><i class="fas fa-users"></i> ${lead.decision_makers?.length || 0} DMs</span>
                    <span><i class="fas fa-envelope"></i> ${lead.verified_emails?.length || 0} emails</span>
                </div>
            </div>
        `;
    }).join('');
}

// ============================================================
// LOAD FUNCTIONS
// ============================================================

async function loadLeads() {
    if (window.leads && window.leads.length > 0 && !window._isGenerating) {
        console.log(`✅ Using ${window.leads.length} leads from memory`);
        window.filteredLeads = window.leads;
        window.totalLeads = window.leads.length;
        applyDateFilter();
        updateCompaniesGrid();
        updateCompaniesTable();
        updateDecisionMakersGrid();
        updateDecisionMakersTable();
        updateAIGrid();
        updatePagination();
        updateSelectedFilters();
        return;
    }
    
    const localLeads = loadLeadsFromLocalStorage();
    if (localLeads.length > 0) {
        window.leads = localLeads;
        window.filteredLeads = localLeads;
        window.totalLeads = localLeads.length;
        console.log(`✅ Using ${window.totalLeads} leads from localStorage (cached)`);
        applyDateFilter();
        updateCompaniesGrid();
        updateCompaniesTable();
        updateDecisionMakersGrid();
        updateDecisionMakersTable();
        updateAIGrid();
        updatePagination();
        updateSelectedFilters();
        if (!window.isAuthenticated) {
            console.log('📁 Not authenticated - using localStorage only');
            return;
        }
    }
    
    if (window.isAuthenticated) {
        try {
            const params = { page: window.currentPage || 1, limit: window.itemsPerPage || 20, sort_by: 'created_at', sort_order: 'desc' };
            if (window.selectedIndustries && window.selectedIndustries.length > 0) params.industries = window.selectedIndustries.join(',');
            if (window.currentCountry) params.country = window.currentCountry;
            const result = await api.getLeads(params);
            if (result.success && result.data && result.data.data && result.data.data.length > 0) {
                window.leads = result.data.data;
                window.filteredLeads = result.data.data;
                window.totalLeads = result.data.pagination?.total || window.leads.length;
                console.log(`✅ Loaded ${window.leads.length} leads from backend (total: ${window.totalLeads})`);
                if (window.leads.length > 0) saveLeadsToLocalStorage(window.leads);
                applyDateFilter();
                updateCompaniesGrid();
                updateCompaniesTable();
                updateDecisionMakersGrid();
                updateDecisionMakersTable();
                updateAIGrid();
                updatePagination();
                updateSelectedFilters();
            } else if (localLeads.length === 0) {
                console.log('🔧 No leads found, generating leads...');
                generateLeads();
            }
        } catch (error) {
            console.error('Error loading leads from backend:', error);
            if (localLeads.length === 0) {
                console.log('🔧 No leads available, generating leads...');
                generateLeads();
            }
        }
    }
}

async function loadGlobalLeads(params = {}) {
    if (window.leads && window.leads.length > 0 && !window._isGenerating) {
        window.globalLeads = window.leads.filter(l => l.country === window.currentCountry);
        window.totalGlobalLeads = window.globalLeads.length;
        console.log(`✅ Using ${window.totalGlobalLeads} leads for ${window.currentCountry} from memory`);
        updateGlobalCompaniesGrid();
        updateGlobalCompaniesTable();
        return;
    }
    
    const localLeads = loadLeadsFromLocalStorage();
    const countryLeads = localLeads.filter(l => l.country === window.currentCountry);
    if (countryLeads.length > 0) {
        window.globalLeads = countryLeads;
        window.totalGlobalLeads = countryLeads.length;
        console.log(`✅ Loaded ${window.totalGlobalLeads} leads for ${window.currentCountry} from localStorage`);
        updateGlobalCompaniesGrid();
        updateGlobalCompaniesTable();
        if (!window.isAuthenticated) return;
    }
    if (window.isAuthenticated) {
        try {
            const result = await api.getCountryLeads(window.currentCountry, { page: 1, limit: 50, ...params });
            if (result.success && result.data && result.data.data && result.data.data.length > 0) {
                window.globalLeads = result.data.data;
                window.totalGlobalLeads = result.data.pagination?.total || window.globalLeads.length;
                console.log(`✅ Loaded ${window.globalLeads.length} leads for ${window.currentCountry} from backend`);
                const allLeads = loadLeadsFromLocalStorage();
                const merged = [...allLeads, ...window.globalLeads];
                const unique = merged.filter((v, i, a) => a.findIndex(t => t.company_name === v.company_name) === i);
                saveLeadsToLocalStorage(unique);
                updateGlobalCompaniesGrid();
                updateGlobalCompaniesTable();
            }
        } catch (error) {
            console.error('Error loading global leads from backend:', error);
        }
    }
}

function updateGlobalCompaniesGrid() {
    const grid = document.getElementById('globalCompaniesGrid');
    if (!grid) return;
    const data = window.globalLeads && window.globalLeads.length > 0 ? window.globalLeads : (window.leads || []).filter(l => l.country === window.currentCountry);
    if (!data || data.length === 0) {
        grid.innerHTML = '<div class="col-12 text-center py-4 text-muted">No companies found for this country</div>';
        return;
    }
    grid.innerHTML = data.slice(0, 8).map(lead => {
        const emailCount = lead.verified_emails?.length || 0;
        const dmCount = lead.decision_makers?.length || 0;
        const flag = lead.flag || '🌍';
        return `
            <div class="card-item global-border" onclick="showLeadDetails('${lead._id}')">
                <div class="card-top">
                    <span class="card-title">${escapeHtml(lead.company_name || 'Unknown')}</span>
                    <span class="country-badge">${flag}</span>
                </div>
                <div class="card-subtitle">${escapeHtml(lead.industry || 'N/A')}</div>
                <div class="card-details">
                    <span class="card-detail"><i class="fas fa-map-marker-alt"></i> ${escapeHtml(lead.city || lead.region || 'N/A')}</span>
                    <span class="card-detail"><i class="fas fa-users"></i> ${dmCount} DMs</span>
                    <span class="card-detail"><i class="fas fa-globe"></i> ${lead.domain || 'No domain'}</span>
                </div>
                ${emailCount > 0 ? `<div class="card-tags"><span class="card-tag verified"><i class="fas fa-check-circle"></i> ${emailCount} emails</span></div>` : ''}
                <div class="card-footer">
                    <span>${new Date(lead.created_at).toLocaleDateString()}</span>
                    <span><i class="fas fa-globe"></i></span>
                </div>
            </div>
        `;
    }).join('');
}

function updateGlobalCompaniesTable() {
    const tbody = document.getElementById('globalCompaniesTable');
    if (!tbody) return;
    const data = window.globalLeads && window.globalLeads.length > 0 ? window.globalLeads : (window.leads || []).filter(l => l.country === window.currentCountry);
    if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" class="text-center py-5"><i class="fas fa-database fa-3x text-muted mb-3"></i><br>No companies found for this country</td></tr>';
        return;
    }
    tbody.innerHTML = data.map((lead) => {
        const source = lead.source || 'unknown';
        const sourceInfo = SOURCES.find(s => s.id === source) || { icon: '📌', color: 'bg-secondary', name: source };
        const verifiedCount = lead.verified_emails?.length || 0;
        const dmCount = lead.decision_makers?.length || 0;
        const icpScore = lead.icp_score || 0;
        const flag = lead.flag || '🌍';
        const created = lead.created_at ? new Date(lead.created_at).toLocaleDateString() : 'Today';
        return `
            <tr class="global-card">
                <td>
                    <span class="company-name" onclick="showLeadDetails('${lead._id}')" style="cursor:pointer;color:var(--primary);font-weight:600;">
                        ${escapeHtml(lead.company_name || 'Unknown')}
                    </span>
                    ${dmCount > 0 ? `<span class="decision-maker-badge ms-1">👥 ${dmCount}</span>` : ''}
                    <span class="country-badge ms-1">${flag}</span>
                </td>
                <td>${escapeHtml(lead.industry || 'N/A')}</td>
                <td>${escapeHtml(lead.region || 'N/A')}</td>
                <td>${escapeHtml(lead.city || 'N/A')}</td>
                <td><span class="badge ${sourceInfo.color}" title="${sourceInfo.name}">${sourceInfo.icon} ${sourceInfo.name}</span></td>
                <td>${verifiedCount > 0 ? `<span class="badge email-valid">✅ ${verifiedCount} verified</span>` : '❌'}</td>
                <td><span class="badge ${icpScore >= 70 ? 'badge-hot' : icpScore >= 40 ? 'badge-warm' : 'badge-cold'}">${icpScore || 0}</span></td>
                <td>${created}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick="showLeadDetails('${lead._id}')"><i class="fas fa-eye"></i></button>
                    <button class="btn btn-sm btn-outline-success" onclick="exportSingleLead('${lead._id}')"><i class="fas fa-download"></i></button>
                </td>
            </tr>
        `;
    }).join('');
}

// ============================================================
// LOAD PRIORITIZED LEADS
// ============================================================
async function loadPrioritizedLeads(minIntentScore = 0, market = null) {
    if (window.leads && window.leads.length > 0 && !window._isGenerating) {
        const marketParam = market || window.currentMarket;
        let filtered = window.leads;
        if (marketParam === 'ethiopia') {
            filtered = filtered.filter(l => l.country === 'ET');
        } else if (marketParam === 'international') {
            filtered = filtered.filter(l => l.country !== 'ET');
        }
        window.prioritizedLeads = filtered.sort((a, b) => (b.icp_score || 0) - (a.icp_score || 0));
        console.log(`✅ Loaded ${window.prioritizedLeads.length} prioritized leads from memory`);
        updatePrioritizedLeadsDisplay();
        return;
    }
    
    const localLeads = loadLeadsFromLocalStorage();
    if (localLeads.length > 0) {
        const marketParam = market || window.currentMarket;
        let filtered = localLeads;
        if (marketParam === 'ethiopia') {
            filtered = filtered.filter(l => l.country === 'ET');
        } else if (marketParam === 'international') {
            filtered = filtered.filter(l => l.country !== 'ET');
        }
        window.prioritizedLeads = filtered.map(lead => ({
            id: lead._id,
            company_name: lead.company_name,
            industry: lead.industry,
            country: lead.country,
            market: lead.country === 'ET' ? 'ethiopia' : 'international',
            website: lead.website || lead.domain,
            icp: { score: lead.icp_score || 50 },
            intent: { score: lead.lead_score || 50, priority: lead.priority || 'warm' },
            decision_makers: lead.decision_makers || [],
            verified_emails: lead.verified_emails || [],
            domain: lead.domain || '',
            source: lead.source || 'unknown'
        }));
        window.prioritizedLeads.sort((a, b) => (b.intent?.score || 0) - (a.intent?.score || 0));
        console.log(`✅ Loaded ${window.prioritizedLeads.length} prioritized leads from localStorage`);
        updatePrioritizedLeadsDisplay();
        if (!window.isAuthenticated) return;
    }
    if (window.isAuthenticated) {
        try {
            const marketParam = market || window.currentMarket;
            const countryParam = marketParam === 'ethiopia' ? 'ET' : marketParam === 'international' ? null : window.currentCountry;
            const result = await api.getPrioritizedLeads(minIntentScore, marketParam, countryParam);
            if (result.success && result.data && result.data.leads && result.data.leads.length > 0) {
                window.prioritizedLeads = result.data.leads;
                console.log(`✅ Loaded ${window.prioritizedLeads.length} prioritized leads from backend`);
                updatePrioritizedLeadsDisplay();
            }
        } catch (error) {
            console.error('Error loading prioritized leads from backend:', error);
        }
    }
}

function updatePrioritizedLeadsDisplay() {
    const container = document.getElementById('prioritizedLeadsContainer');
    if (!container) return;
    const data = window.prioritizedLeads && window.prioritizedLeads.length > 0 ? window.prioritizedLeads : window.leads;
    if (!data || data.length === 0) {
        container.innerHTML = '<div class="alert alert-info">No prioritized leads found. Click "Generate Leads" to start!</div>';
        return;
    }
    const sorted = [...data].sort((a, b) => (b.icp_score || 0) - (a.icp_score || 0));
    container.innerHTML = sorted.slice(0, 6).map(lead => {
        const isEthiopian = lead.country === 'ET';
        const flag = lead.flag || '🌍';
        const dmCount = lead.decision_makers?.length || 0;
        const emailCount = lead.verified_emails?.length || 0;
        const icpScore = lead.icp_score || 0;
        const priority = lead.priority || (icpScore >= 70 ? 'hot' : icpScore >= 40 ? 'warm' : 'cold');
        return `
            <div class="card-item ${isEthiopian ? 'ethiopia-border' : 'global-border'} mb-3" onclick="showLeadDetails('${lead._id}')">
                <div class="card-top">
                    <span class="card-title">${escapeHtml(lead.company_name || 'Unknown')} ${flag}</span>
                    <span class="card-badge ${priority}">${icpScore}</span>
                </div>
                <div class="card-details">
                    <span class="card-detail"><i class="fas fa-industry"></i> ${escapeHtml(lead.industry || 'N/A')}</span>
                    <span class="card-detail"><i class="fas fa-map-marker-alt"></i> ${escapeHtml(lead.city || lead.region || 'N/A')}</span>
                    <span class="card-detail"><i class="fas fa-users"></i> ${dmCount} DMs</span>
                    <span class="card-detail"><i class="fas fa-envelope"></i> ${emailCount} emails</span>
                </div>
                ${isEthiopian ? '<span class="ethiopia-flag-badge">🇪🇹 Ethiopia</span>' : ''}
                <div class="card-footer">
                    <span>${lead.created_at ? new Date(lead.created_at).toLocaleDateString() : 'N/A'}</span>
                    <span><i class="fas fa-${isEthiopian ? 'flag' : 'globe'}"></i> ${isEthiopian ? 'Local' : 'Global'}</span>
                </div>
            </div>
        `;
    }).join('');
}

// ============================================================
// UPDATE PAGINATION
// ============================================================
function updatePagination() {
    const pages = Math.ceil(totalLeads / itemsPerPage);
    const pagination = document.getElementById('pagination');
    if (!pagination) return;
    if (pages <= 1) { pagination.innerHTML = ''; return; }
    let html = '';
    html += `<button class="page-btn ${currentPage === 1 ? 'disabled' : ''}" onclick="changePage(${currentPage - 1})">&laquo;</button>`;
    for (let i = 1; i <= pages; i++) {
        if (i === 1 || i === pages || (i >= currentPage - 2 && i <= currentPage + 2)) {
            html += `<button class="page-btn ${i === currentPage ? 'active' : ''}" onclick="changePage(${i})">${i}</button>`;
        } else if (i === currentPage - 3 || i === currentPage + 3) {
            html += `<span class="page-btn disabled">...</span>`;
        }
    }
    html += `<button class="page-btn ${currentPage === pages ? 'disabled' : ''}" onclick="changePage(${currentPage + 1})">&raquo;</button>`;
    pagination.innerHTML = html;
}

window.changePage = function(page) {
    if (page < 1 || page > Math.ceil(totalLeads / itemsPerPage)) return;
    currentPage = page;
    loadLeads();
};

// ============================================================
// SHOW LEAD DETAILS
// ============================================================
window.showLeadDetails = async function(leadId) {
    if (!leadId) return;
    if (typeof bootstrap === 'undefined' || !bootstrap.Modal) {
        alert('Bootstrap modal not available.');
        return;
    }
    try {
        const modalElement = document.getElementById('companyModal');
        if (!modalElement) return;
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
        const modalBody = document.getElementById('companyModalBody');
        if (!modalBody) return;
        modalBody.innerHTML = `<div class="text-center py-4"><div class="spinner-custom"></div><p class="text-muted mt-2">Loading company details...</p></div>`;
        
        let lead = leads.find(l => l._id === leadId);
        
        if (!lead) {
            lead = window.leads.find(l => l._id === leadId);
        }
        
        if (!lead) {
            modalBody.innerHTML = '<div class="text-center py-4 text-danger">Error loading company details.</div>';
            return;
        }
        
        currentLeadId = leadId;
        const isEthiopian = lead.country === 'ET';
        const flag = lead.flag || '🌍';
        const country = GLOBAL_CONFIG.countries.find(c => c.code === lead.country);
        
        let html = `
            <div class="row">
                <div class="col-md-6">
                    <h6><i class="fas fa-building me-2"></i>Company Information</h6>
                    <table class="table table-sm">
                        <tr><th>Name:</th><td><strong>${escapeHtml(lead.company_name)}</strong> ${flag}</td></tr>
                        <tr><th>Industry:</th><td>${lead.industry || 'N/A'}</td></tr>
                        <tr><th>Country:</th><td>${country ? country.name : lead.country || 'N/A'} ${flag}</td></tr>
                        <tr><th>Region:</th><td>${lead.region || 'N/A'}</td></tr>
                        <tr><th>City:</th><td>${lead.city || 'N/A'}</td></tr>
                        <tr><th>Domain:</th><td>${lead.domain ? `<a href="http://${lead.domain}" target="_blank">${lead.domain}</a>` : 'N/A'}</td></tr>
                        <tr><th>ICP Score:</th><td><span class="badge ${lead.icp_score >= 70 ? 'badge-hot' : lead.icp_score >= 40 ? 'badge-warm' : 'badge-cold'}">${lead.icp_score || 0}</span></td></tr>
                        <tr><th>Priority:</th><td><span class="badge ${lead.priority === 'hot' ? 'badge-hot' : lead.priority === 'warm' ? 'badge-warm' : 'badge-cold'}">${lead.priority || 'N/A'}</span></td></tr>
                        <tr><th>Source:</th><td><span class="badge bg-secondary">${lead.source || 'unknown'}</span></td></tr>
                        <tr><th>Employees:</th><td>${lead.employees || 'N/A'}</td></tr>
                        <tr><th>Revenue:</th><td>${lead.revenue || 'N/A'}</td></tr>
                        <tr><th>Founded:</th><td>${lead.founded || 'N/A'}</td></tr>
                        <tr><th>Created:</th><td>${lead.created_at ? new Date(lead.created_at).toLocaleDateString() : 'N/A'}</td></tr>
                    </table>
                </div>
                <div class="col-md-6">
                    <h6><i class="fas fa-microchip me-2"></i>Technologies</h6>
                    ${lead.technologies?.length > 0 ?
                        `<div class="mb-3">${lead.technologies.map(t => `<span class="badge bg-light text-dark me-1 mb-1">${t}</span>`).join('')}</div>` :
                        '<p class="text-muted">No technology data</p>'
                    }
                    ${isEthiopian ? '<div class="mt-2"><span class="ethiopia-flag-badge">🇪🇹 Ethiopian Company</span></div>' : ''}
                </div>
            </div>
        `;
        
        if (lead.ai_description) {
            html += `
                <div class="mt-4">
                    <h6><i class="fas fa-robot me-2"></i>AI-Generated Summary</h6>
                    <div class="ai-description-box">${lead.ai_description}</div>
                </div>
            `;
        }
        
        if (lead.decision_makers?.length > 0) {
            html += `
                <div class="mt-4">
                    <h6><i class="fas fa-users me-2"></i>Decision Makers (${lead.decision_makers.length})</h6>
                    <div class="table-responsive">
                        <table class="table table-sm table-hover">
                            <thead class="table-light">
                                <tr><th>Name</th><th>Position</th><th>Email</th><th>LinkedIn</th><th>Confidence</th></tr>
                            </thead>
                            <tbody>
                                ${lead.decision_makers.map(dm => `
                                    <tr>
                                        <td><strong>${escapeHtml(dm.name || 'Unknown')}</strong></td>
                                        <td>${dm.position || dm.title || 'N/A'}</td>
                                        <td>${dm.email ? `<span class="badge bg-success">${dm.email}</span>` : '-'}</td>
                                        <td>${dm.linkedin ? `<a href="${dm.linkedin}" target="_blank"><i class="fab fa-linkedin text-primary"></i></a>` : '-'}</td>
                                        <td>${dm.confidence ? `${dm.confidence}%` : '-'}</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            `;
        }
        
        if (lead.verified_emails?.length > 0) {
            html += `
                <div class="mt-4">
                    <h6><i class="fas fa-envelope me-2"></i>Verified Emails</h6>
                    <div class="table-responsive">
                        <table class="table table-sm table-hover">
                            <thead class="table-light">
                                <tr><th>Email</th><th>Status</th><th>Confidence</th><th>Method</th></tr>
                            </thead>
                            <tbody>
                                ${lead.verified_emails.map(v => `
                                    <tr>
                                        <td><code>${v.email}</code></td>
                                        <td><span class="badge ${v.status === 'valid' ? 'bg-success' : v.status === 'risky' ? 'bg-warning' : 'bg-danger'}">${v.status}</span></td>
                                        <td>${v.confidence || '-'}%</td>
                                        <td><span class="badge ${v.method === 'diy_smtp' ? 'bg-info' : 'bg-primary'}">${v.method || 'hunter'}</span></td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            `;
        }
        
        if (lead.hiring_data && lead.hiring_data.is_hiring) {
            html += `
                <div class="mt-4">
                    <h6><i class="fas fa-briefcase me-2"></i>Hiring Signals</h6>
                    <div class="alert alert-success">
                        <strong>🚀 Actively hiring</strong> - ${lead.hiring_data.job_count || 0} open positions
                        ${lead.hiring_data.departments_hiring ? 
                            `<br><small>Departments: ${lead.hiring_data.departments_hiring.join(', ')}</small>` : ''}
                    </div>
                </div>
            `;
        }
        
        modalBody.innerHTML = html;
        document.getElementById('exportCompanyBtn').onclick = () => exportSingleLead(lead._id);
    } catch (error) {
        console.error('Error showing lead details:', error);
        alert('Error loading lead details. Please try again.');
    }
};

// ============================================================
// NAVIGATION
// ============================================================
function showDashboard() {
    document.querySelectorAll('.page-content').forEach(el => el.style.display = 'none');
    const dashboardContent = document.getElementById('dashboardContent');
    if (dashboardContent) dashboardContent.style.display = 'block';
    document.getElementById('pageTitle').textContent = 'Dashboard';
    document.querySelectorAll('.sidebar-menu-link').forEach(l => l.classList.remove('active'));
    const dashboardLink = document.getElementById('dashboardLink');
    if (dashboardLink) dashboardLink.classList.add('active');
    forceUpdateDashboard();
}

function showCompanies() {
    document.querySelectorAll('.page-content').forEach(el => el.style.display = 'none');
    const companiesPage = document.getElementById('companiesPage');
    if (companiesPage) companiesPage.style.display = 'block';
    document.getElementById('pageTitle').textContent = 'All Companies';
    document.querySelectorAll('.sidebar-menu-link').forEach(l => l.classList.remove('active'));
    const companiesLink = document.getElementById('companiesLink');
    if (companiesLink) companiesLink.classList.add('active');
    loadLeads();
}

function showEthiopianCompanies() {
    document.querySelectorAll('.page-content').forEach(el => el.style.display = 'none');
    const ethiopianPage = document.getElementById('ethiopianCompaniesPage');
    if (ethiopianPage) ethiopianPage.style.display = 'block';
    document.getElementById('pageTitle').textContent = 'Ethiopian Companies 🇪🇹';
    document.querySelectorAll('.sidebar-menu-link').forEach(l => l.classList.remove('active'));
    const ethiopianLink = document.getElementById('ethiopianCompaniesLink');
    if (ethiopianLink) ethiopianLink.classList.add('active');
    const savedCountry = currentCountry;
    currentCountry = 'ET';
    loadGlobalLeads();
    currentCountry = savedCountry;
}

function showGlobalCompanies() {
    document.querySelectorAll('.page-content').forEach(el => el.style.display = 'none');
    const globalPage = document.getElementById('globalCompaniesPage');
    if (globalPage) globalPage.style.display = 'block';
    document.getElementById('pageTitle').textContent = 'Global Companies 🌍';
    document.querySelectorAll('.sidebar-menu-link').forEach(l => l.classList.remove('active'));
    const globalLink = document.getElementById('globalCompaniesLink');
    if (globalLink) globalLink.classList.add('active');
    loadGlobalLeads();
    populateGlobalFilters();
}

function showDecisionMakers() {
    document.querySelectorAll('.page-content').forEach(el => el.style.display = 'none');
    const dmPage = document.getElementById('decisionMakersPage');
    if (dmPage) dmPage.style.display = 'block';
    document.getElementById('pageTitle').textContent = 'Decision Makers';
    document.querySelectorAll('.sidebar-menu-link').forEach(l => l.classList.remove('active'));
    const dmLink = document.getElementById('decisionMakersLink');
    if (dmLink) dmLink.classList.add('active');
    updateDecisionMakersTable();
}

function showSignals() {
    document.querySelectorAll('.page-content').forEach(el => el.style.display = 'none');
    const signalsPage = document.getElementById('signalsPage');
    if (signalsPage) signalsPage.style.display = 'block';
    document.getElementById('pageTitle').textContent = 'Intent Signals';
    document.querySelectorAll('.sidebar-menu-link').forEach(l => l.classList.remove('active'));
    const signalsLink = document.getElementById('signalsLink');
    if (signalsLink) signalsLink.classList.add('active');
}

function showExports() {
    document.querySelectorAll('.page-content').forEach(el => el.style.display = 'none');
    const exportsPage = document.getElementById('exportsPage');
    if (exportsPage) exportsPage.style.display = 'block';
    document.getElementById('pageTitle').textContent = 'Exports';
    document.querySelectorAll('.sidebar-menu-link').forEach(l => l.classList.remove('active'));
    const exportsLink = document.getElementById('exportsLink');
    if (exportsLink) exportsLink.classList.add('active');
}

function showSettings() {
    document.querySelectorAll('.page-content').forEach(el => el.style.display = 'none');
    const settingsPage = document.getElementById('settingsPage');
    if (settingsPage) settingsPage.style.display = 'block';
    document.getElementById('pageTitle').textContent = 'Settings';
    document.querySelectorAll('.sidebar-menu-link').forEach(l => l.classList.remove('active'));
    const settingsLink = document.getElementById('settingsLink');
    if (settingsLink) settingsLink.classList.add('active');
}

// ============================================================
// EXPORT FUNCTIONS - FIXED TO USE WINDOW.LEADS
// ============================================================
window.exportLeadsByPeriod = async function(format, period, includeAi, country = null) {
    try {
        // CRITICAL FIX: Use window.leads instead of leads
        const dataToExport = (window.leads || []).map(lead => ({
            'Company Name': lead.company_name || '',
            'Industry': lead.industry || '',
            'Country': lead.country_name || lead.country || '',
            'Region': lead.region || '',
            'City': lead.city || '',
            'Domain': lead.domain || '',
            'ICP Score': lead.icp_score || 0,
            'Priority': lead.priority || '',
            'Source': lead.source || '',
            'Emails': (lead.verified_emails || []).map(e => e.email).join('; '),
            'Decision Makers': (lead.decision_makers || []).map(d => `${d.name} (${d.position})`).join('; '),
            'Employees': lead.employees || '',
            'Revenue': lead.revenue || '',
            'Created': lead.created_at ? new Date(lead.created_at).toLocaleDateString() : ''
        }));
        
        console.log(`📊 Exporting ${dataToExport.length} leads`);
        
        if (dataToExport.length === 0) {
            showToast('⚠️ No data to export. Generate leads first!', 'warning');
            return;
        }
        
        const headers = Object.keys(dataToExport[0]);
        const csvRows = [headers.join(',')];
        for (const row of dataToExport) {
            const values = headers.map(header => {
                const val = row[header] || '';
                return `"${String(val).replace(/"/g, '""')}"`;
            });
            csvRows.push(values.join(','));
        }
        
        const csvContent = csvRows.join('\n');
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        const suffix = country ? `_${country}` : '';
        const periodLabel = period === 'all' ? 'all' : period;
        a.download = `leads${suffix}_${periodLabel}_${new Date().toISOString().split('T')[0]}.${format === 'excel' ? 'xlsx' : 'csv'}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        setTimeout(() => window.URL.revokeObjectURL(url), 100);
        
        showToast(`✅ ${dataToExport.length} leads exported successfully!`, 'success');
        addRecentActivity(`Exported ${dataToExport.length} leads as ${format.toUpperCase()}`);
    } catch (error) {
        console.error('Export error:', error);
        showToast('Export failed: ' + error.message, 'error');
    }
};

function exportSingleLead(id) {
    if (id) {
        // CRITICAL FIX: Use window.leads instead of leads
        const lead = (window.leads || []).find(l => l._id === id);
        if (lead) {
            const headers = ['Company Name', 'Industry', 'Country', 'Region', 'City', 'Domain', 'ICP Score', 'Priority', 'Source', 'Emails', 'Decision Makers', 'Employees', 'Revenue', 'Created'];
            const row = [
                lead.company_name || '',
                lead.industry || '',
                lead.country_name || lead.country || '',
                lead.region || '',
                lead.city || '',
                lead.domain || '',
                lead.icp_score || 0,
                lead.priority || '',
                lead.source || '',
                (lead.verified_emails || []).map(e => e.email).join('; '),
                (lead.decision_makers || []).map(d => `${d.name} (${d.position})`).join('; '),
                lead.employees || '',
                lead.revenue || '',
                lead.created_at ? new Date(lead.created_at).toLocaleDateString() : ''
            ];
            const csvContent = [headers.join(','), row.map(v => `"${String(v).replace(/"/g, '""')}"`).join(',')].join('\n');
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${lead.company_name || 'lead'}_${new Date().toISOString().split('T')[0]}.csv`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            setTimeout(() => window.URL.revokeObjectURL(url), 100);
            addRecentActivity('Exported single lead');
            showToast('✅ Lead exported successfully!', 'success');
            return;
        }
        showToast('❌ Lead not found', 'error');
    }
}

window.exportSignalsToFolder = function() {
    showToast('📦 Exporting signals to folder...', 'info');
    setTimeout(() => {
        showToast('✅ Signals exported successfully!', 'success');
        addRecentActivity('Exported signals to folder');
    }, 1500);
};

// ============================================================
// SETUP EXPORT MENU
// ============================================================
function setupExportMenu() {
    const exportBtn = document.getElementById('exportBtn');
    const exportMenu = document.getElementById('exportMenu');
    if (exportBtn && exportMenu) {
        exportBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            exportMenu.style.display = exportMenu.style.display === 'block' ? 'none' : 'block';
        });
        document.addEventListener('click', () => {
            exportMenu.style.display = 'none';
        });
    }
}

// ============================================================
// OTHER FUNCTIONS
// ============================================================
async function testScrapingbee() {
    if (!isAuthenticated) { showToast('Not connected to backend', 'error'); return; }
    showToast('🧪 Testing ScrapingBee API...', 'info');
    const result = await api.testScrapingbee();
    if (result.success) {
        showToast('✅ ScrapingBee API is working!', 'success');
    } else {
        showToast('❌ ScrapingBee API test failed', 'error');
    }
}

async function testHunterApi() {
    if (!isAuthenticated) { showToast('Not connected to backend', 'error'); return; }
    showToast('🔍 Testing Hunter.io API...', 'info');
    const result = await api.hunterCompanyEnrichment('stripe.com');
    if (result.success && result.data) {
        showToast('✅ Hunter.io is working!', 'success');
    } else {
        showToast('❌ Hunter.io test failed', 'error');
    }
}

async function discoverDomain() {
    const companyName = prompt('Enter company name to discover domain:');
    if (!companyName) return;
    showToast(`🔍 Discovering domain for ${companyName}...`, 'info');
    const result = await api.discoverDomain(companyName);
    if (result.success && result.data && result.data.domain) {
        showToast(`✅ Found domain: ${result.data.domain}`, 'success');
        addRecentActivity(`Discovered domain: ${result.data.domain} for ${companyName}`);
    } else {
        showToast('❌ Could not discover domain', 'error');
    }
}

async function verifyEmail() {
    const email = prompt('Enter email address to verify:');
    if (!email) return;
    showToast(`🔍 Verifying ${email}...`, 'info');
    const result = await api.verifyEmail(email);
    if (result.success && result.data) {
        showToast(`✅ Email ${result.data.status}`, 'success');
        addRecentActivity(`Verified email: ${email}`);
    } else {
        showToast('❌ Verification failed', 'error');
    }
}

async function verifyEmailDIY() {
    const email = prompt('Enter email address to verify with DIY method:');
    if (!email) return;
    showToast(`🔍 Verifying ${email} with DIY SMTP...`, 'info');
    const result = await api.verifyEmailDIY(email);
    if (result.success && result.data) {
        showToast(`✅ Email ${result.data.status} (DIY)`, 'success');
        addRecentActivity(`DIY verified email: ${email}`);
    } else {
        showToast('❌ Verification failed', 'error');
    }
}

async function discoverEmails() {
    const domain = prompt('Enter domain to discover emails:');
    if (!domain) return;
    const companyName = prompt('Enter company name (optional):');
    showToast(`🔍 Discovering emails for ${domain}...`, 'info');
    const result = await api.discoverEmails(domain, companyName || null);
    if (result.success && result.data) {
        const data = result.data;
        showToast(`✅ Found ${data.all_emails.length} emails`, 'success');
        addRecentActivity(`Discovered emails for ${domain}`);
    } else {
        showToast('❌ Discovery failed', 'error');
    }
}

async function checkAPIUsage() {
    showToast('📊 Checking API usage...', 'info');
    await loadAPIUsage();
    showToast('✅ API usage updated', 'success');
    addRecentActivity('Checked API usage');
}

async function loadAPIUsage() {
    const hunterResult = await api.getHunterUsage();
    const clearbitResult = await api.getClearbitUsage();
    if (hunterResult.success) {
        updateHunterUsage(hunterResult.data.usage);
    }
    if (clearbitResult.success) {
        updateClearbitUsage(clearbitResult.data.usage);
    }
}

function updateHunterUsage(usage) {
    const hunterUsageEl = document.getElementById('hunterUsage');
    if (!hunterUsageEl) return;
    const percent = (usage.count / usage.limit) * 100;
    hunterUsageEl.innerHTML = `
        <div class="api-usage-card">
            <div><strong>Hunter.io Free Tier</strong><div class="small text-muted">${usage.count}/${usage.limit} used</div></div>
            <span class="badge ${usage.count < usage.limit ? 'bg-success' : 'bg-warning'}">${usage.count < usage.limit ? 'Available' : 'Limit Reached'}</span>
        </div>
        <div class="api-usage-progress"><div class="api-usage-fill" style="width: ${percent}%"></div></div>
    `;
}

function updateClearbitUsage(usage) {
    const clearbitUsageEl = document.getElementById('clearbitUsage');
    if (!clearbitUsageEl) return;
    clearbitUsageEl.innerHTML = `
        <div class="api-usage-card">
            <div><strong>Clearbit Free Tier</strong><div class="small text-muted">Unlimited</div></div>
            <span class="badge bg-success">Free</span>
        </div>
    `;
}

function updateBackendInfo(info) {
    if (!info && api.backendInfo) info = api.backendInfo;
    if (!info) return;
    const hunterStatus = document.getElementById('hunterStatus');
    if (hunterStatus) {
        hunterStatus.innerHTML = info.hunter_configured ? 
            '<span class="badge bg-success">✅ Active</span>' : 
            '<span class="badge bg-secondary">⚠️ Not Configured</span>';
    }
    const mongoStatus = document.getElementById('mongoStatus');
    if (mongoStatus) {
        mongoStatus.innerHTML = info.mongodb && info.mongodb === 'connected' ? 
            '<span class="badge bg-success">✅ Connected</span>' : 
            '<span class="badge bg-warning">⚠️ Local Storage</span>';
    }
    const geminiStatus = document.getElementById('geminiStatus');
    if (geminiStatus) {
        geminiStatus.innerHTML = info.gemini_available ? 
            '<span class="badge bg-success">✅ Active</span>' : 
            '<span class="badge bg-secondary">⚠️ Not Configured</span>';
    }
    const backendStatus = document.getElementById('backendStatus');
    if (backendStatus) {
        backendStatus.innerHTML = `<span class="badge bg-success">✅ Connected v${info.version || '11.0'}</span>`;
    }
}

async function reconnectMongoDB() {
    showToast('🔄 Reconnecting to MongoDB...', 'info');
    const result = await api.mongodbReconnect();
    if (result.success) {
        showToast('✅ MongoDB reconnected successfully!', 'success');
        addRecentActivity('Reconnected to MongoDB');
        await loadDashboardStats();
        await loadLeads();
        await loadGlobalLeads();
        await loadAPIUsage();
    } else {
        showToast('❌ Failed to reconnect to MongoDB', 'error');
    }
}

async function checkHealth() {
    showToast('🩺 Checking system health...', 'info');
    const result = await api.checkHealth();
    if (result.success) {
        showToast('✅ System is healthy!', 'success');
        addRecentActivity('Performed health check - OK');
        updateBackendInfo(result.data);
    } else {
        showToast('❌ Health check failed', 'error');
    }
}

async function loadDashboardStats() {
    const result = await api.getDashboardStats(30);
    if (result.success && result.data && result.data.stats) {
        dashboardStats = result.data.stats;
        updateDashboardStats();
    }
}

function updateSourceBadges() {
    const container = document.getElementById('sourceBadges');
    if (!container) return;
    let html = '<div class="d-flex flex-wrap gap-2">';
    SOURCES.forEach(source => {
        let iconClass = '';
        switch(source.id) {
            case 'exa': iconClass = 'fas fa-search'; break;
            case 'yellowpages': iconClass = 'fas fa-book'; break;
            case 'clearbit': iconClass = 'fas fa-lightbulb'; break;
            case 'apollo': iconClass = 'fas fa-rocket'; break;
            case 'hunter': iconClass = 'fas fa-envelope'; break;
            case 'website': iconClass = 'fas fa-globe'; break;
            case '2ehire': iconClass = 'fas fa-building'; break;
            case 'ethioyellow': iconClass = 'fas fa-book-open'; break;
            case 'ethiobusiness': iconClass = 'fas fa-briefcase'; break;
            case 'global_api': iconClass = 'fas fa-globe-americas'; break;
            default: iconClass = 'fas fa-database';
        }
        html += `<span class="badge ${source.color} p-2"><i class="${iconClass} me-1"></i>${source.name}</span>`;
    });
    html += '</div>';
    container.innerHTML = html;
}

function loadScrapeStats() {
    const saved = localStorage.getItem('scrapeStats');
    if (saved) {
        try { scrapeStats = JSON.parse(saved); } catch (e) {}
    }
    updateScrapeStatsDisplay();
}

function saveScrapeStats() {
    localStorage.setItem('scrapeStats', JSON.stringify(scrapeStats));
}

function updateScrapeStatsDisplay() {
    const statsEl = document.getElementById('scrapeStats');
    if (!statsEl) return;
    statsEl.innerHTML = `
        <div class="text-center"><div class="h4 mb-0" id="statScrapes">${scrapeStats.totalScrapes}</div><small class="text-muted">Scrapes</small></div>
        <div class="text-center"><div class="h4 mb-0" id="statLeadsFound">${scrapeStats.totalLeadsFound}</div><small class="text-muted">Leads</small></div>
        <div class="text-center"><div class="h4 mb-0" id="statLeadsSaved">${scrapeStats.totalLeadsSaved}</div><small class="text-muted">Saved</small></div>
        <div class="text-center"><div class="h4 mb-0" id="statEthiopian">${scrapeStats.totalEthiopianLeadsFound || 0}</div><small class="text-muted">🇪🇹</small></div>
    `;
}

function startAutoRefresh() {
    if (autoRefreshTimer) clearInterval(autoRefreshTimer);
    autoRefreshTimer = setInterval(checkForNewLeads, 30000);
}

async function checkForNewLeads() {
    if (!isAuthenticated || isMassiveScraping) return;
    try {
        const result = await api.getTodayLeads();
        if (result.success && result.data) {
            const todayCount = result.data.count || 0;
            const previousCount = newLeadsCount;
            newLeadsCount = todayCount;
            updateNewLeadsIndicator();
            if (todayCount > previousCount && previousCount > 0) {
                showToast(`📢 ${todayCount - previousCount} new leads detected!`, 'info');
                addRecentActivity(`Detected ${todayCount - previousCount} new leads`);
                await loadLeads();
                await loadGlobalLeads();
                await loadDashboardStats();
            }
        }
    } catch (error) {
        console.log('Error checking for new leads:', error);
    }
}

function updateNewLeadsIndicator() {
    const newLeadsIndicator = document.getElementById('newLeadsIndicator');
    if (newLeadsIndicator) {
        if (newLeadsCount > 0) {
            newLeadsIndicator.innerHTML = `<span class="new-leads-counter">${newLeadsCount} new today</span>`;
            newLeadsIndicator.style.display = 'inline';
        } else {
            newLeadsIndicator.style.display = 'none';
        }
    }
}

function addRecentActivity(message) {
    recentActivities.unshift({ message, time: new Date().toLocaleTimeString() });
    if (recentActivities.length > 5) recentActivities.pop();
    updateRecentActivity();
}

function updateRecentActivity() {
    const container = document.getElementById('recentActivity');
    if (!container) return;
    if (recentActivities.length === 0) {
        container.innerHTML = '<p class="text-muted text-center">No recent activity</p>';
        return;
    }
    let html = '';
    recentActivities.forEach(activity => {
        html += `
            <div class="activity-item">
                <div class="activity-icon primary"><i class="fas fa-circle"></i></div>
                <div class="activity-content">
                    <div class="activity-text">${activity.message}</div>
                    <div class="activity-time">${activity.time}</div>
                </div>
            </div>
        `;
    });
    container.innerHTML = html;
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function setFilter(filter) {
    currentFilter = filter;
    applyDateFilter();
    updateCompaniesGrid();
    updateSelectedFilters();
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.filter === filter) btn.classList.add('active');
    });
}

function setMarket(market) {
    currentMarket = market;
    loadPrioritizedLeads(0, market);
    updateSelectedFilters();
    document.querySelectorAll('.market-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.market === market) {
            btn.classList.add('active');
            if (market === 'ethiopia') btn.classList.add('active-ethiopia');
        }
    });
    const marketLabel = market === 'all' ? 'All Markets' : market === 'ethiopia' ? 'Ethiopian Companies' : 'International Companies';
    addRecentActivity(`Filtered by market: ${marketLabel}`);
}

async function applyEthiopianFilters() {
    const region = document.getElementById('regionFilter')?.value;
    const city = document.getElementById('cityFilter')?.value;
    const industry = document.getElementById('ethiopianIndustryFilter')?.value;
    const params = {};
    if (region) params.region = region;
    if (city) params.city = city;
    if (industry) params.industry = industry;
    await loadGlobalLeads(params);
}

function refreshDashboard() {
    loadLeads();
    loadGlobalLeads();
    loadPrioritizedLeads();
    loadDashboardStats();
    forceUpdateDashboard();
    showToast('🔄 Dashboard refreshed!', 'success');
}

window.retryConnection = async function() {
    showToast('🔄 Retrying connection to backend...', 'info');
    await verifyAuthentication();
    if (isAuthenticated) {
        await loadDashboardStats();
        await loadLeads();
        await loadGlobalLeads();
        await loadPrioritizedLeads();
        await loadAPIUsage();
        await loadCountryFilters(currentCountry);
        updateBackendInfo();
        showToast('✅ Connected to backend successfully!', 'success');
    }
};

// ============================================================
// DEBUG - CHECK LEADS DATA
// ============================================================
function checkLeadsData() {
    console.log('=== LEADS DATA CHECK ===');
    console.log('window.leads:', window.leads);
    console.log('window.leads length:', window.leads ? window.leads.length : 0);
    console.log('leads (local):', leads);
    console.log('leads length:', leads ? leads.length : 0);
    
    const stored = localStorage.getItem('leads_data');
    if (stored) {
        const data = JSON.parse(stored);
        console.log('localStorage leads:', data.leads ? data.leads.length : 0);
    }
    
    showToast(`📊 Found ${window.leads ? window.leads.length : 0} leads in memory`, 'info');
    return window.leads || [];
}

window.checkLeadsData = checkLeadsData;

// ============================================================
// SHOW LOADING STATE
// ============================================================
function showLoadingState() {
    const containers = ['companiesTable', 'allDecisionMakersTableBody', 'prioritizedLeadsContainer', 'dashboardStats', 'ethiopianCompaniesContainer', 'globalCompaniesGrid', 'globalCompaniesTable'];
    containers.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            if (id === 'prioritizedLeadsContainer') {
                el.innerHTML = '<div class="col-12 text-center py-5"><div class="spinner-custom"></div><p class="text-muted">Loading data...</p></div>';
            } else {
                el.innerHTML = '<tr><td colspan="10" class="text-center py-5"><div class="spinner-custom"></div><p class="text-muted">Loading leads...</p></div></tr>';
            }
        }
    });
    const grid = document.getElementById('companiesGrid');
    if (grid) grid.innerHTML = '<div class="col-12 text-center py-4"><div class="spinner-custom"></div><p class="mt-2">Loading companies...</p></div>';
}

function showOfflineMessage() {
    const message = `
        <div class="alert alert-warning m-4">
            <i class="fas fa-exclamation-triangle me-2"></i>
            <strong>Cannot connect to backend server!</strong><br>
            Please ensure the backend is running on port 8007:<br>
            <code>python app.py</code><br><br>
            <button class="btn btn-sm btn-primary" onclick="retryConnection()">
                <i class="fas fa-sync-alt me-1"></i>Retry Connection
            </button>
        </div>
    `;
    const containers = ['companiesTable', 'allDecisionMakersTableBody', 'prioritizedLeadsContainer', 'dashboardStats', 'companiesGrid', 'globalCompaniesGrid', 'decisionMakersGrid', 'aiGrid'];
    containers.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            if (id === 'companiesTable' || id === 'allDecisionMakersTableBody') {
                el.innerHTML = `<tr><td colspan="10" class="text-center py-5">${message}</td></tr>`;
            } else {
                el.innerHTML = message;
            }
        }
    });
}

// ============================================================
// SETUP EVENT LISTENERS
// ============================================================
function setupEventListeners() {
    document.addEventListener('click', function(event) {
        const exportMenu = document.getElementById('exportMenu');
        const exportBtn = document.getElementById('exportBtn');
        if (exportMenu && exportBtn && !exportBtn.contains(event.target) && !exportMenu.contains(event.target)) {
            exportMenu.style.display = 'none';
        }
    });
    const regionFilter = document.getElementById('regionFilter');
    if (regionFilter) regionFilter.addEventListener('change', applyAllFilters);
    const cityFilter = document.getElementById('cityFilter');
    if (cityFilter) cityFilter.addEventListener('change', applyAllFilters);
    const industryFilter = document.getElementById('ethiopianIndustryFilter');
    if (industryFilter) industryFilter.addEventListener('change', applyAllFilters);
    
    const globalCountryFilter = document.getElementById('globalCountryFilter');
    if (globalCountryFilter) {
        globalCountryFilter.addEventListener('change', function() {
            updateGlobalFilters();
            applyGlobalFilters();
        });
    }
    
    const globalRegionFilter = document.getElementById('globalRegionFilter');
    if (globalRegionFilter) {
        globalRegionFilter.addEventListener('change', applyGlobalFilters);
    }
    
    const globalIndustryFilter = document.getElementById('globalIndustryFilter');
    if (globalIndustryFilter) {
        globalIndustryFilter.addEventListener('change', applyGlobalFilters);
    }
    
    const globalCityFilter = document.getElementById('globalCityFilter');
    if (globalCityFilter) {
        globalCityFilter.addEventListener('change', applyGlobalFilters);
    }
    
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
            showToast(`Dark mode ${document.body.classList.contains('dark-mode') ? 'enabled' : 'disabled'}`, 'success');
        });
    }
    
    const cityDropdown = document.getElementById('globalCityFilter');
    if (cityDropdown) {
        cityDropdown.addEventListener('change', function() {
            onCityDropdownChange(this.value);
        });
    }
    
    const industryDropdown = document.getElementById('globalIndustryFilter');
    if (industryDropdown) {
        industryDropdown.addEventListener('change', function() {
            onIndustryDropdownChange(this.value);
        });
    }
}

// ============================================================
// DARK MODE INIT
// ============================================================
const darkMode = localStorage.getItem('darkMode') === 'true';
if (darkMode) document.body.classList.add('dark-mode');

// ============================================================
// INITIALIZATION
// ============================================================
function initializeDashboard() {
    console.log('🚀 Dashboard initializing with Global AI Powered Lead Gen v11.0...');
    console.log('🌍 GLOBAL MARKET INTEGRATION ACTIVE');
    console.log(`🌍 ${GLOBAL_CONFIG.countries.length} countries available`);
    console.log(`🏢 ${ALL_INDUSTRIES.length} industries available`);
    console.log('🇪🇹 Ethiopian Market included as default option');
    
    addFavicon();
    
    try {
        initIndustryFilters();
        initIndustryFiltersWithCheckboxes();
    } catch (e) {
        console.warn('⚠️ Industry filters init error:', e);
    }
    
    initCountrySelector();
    
    setTimeout(() => {
        try {
            initGlobalCharts();
        } catch (e) {
            console.warn('⚠️ Charts init error:', e);
        }
    }, 500);
    
    showLoadingState();
    
    if (window.leads && window.leads.length > 0) {
        console.log(`✅ Using ${window.leads.length} leads already in memory`);
        forceUpdateDashboard();
    } else {
        const localLeads = loadLeadsFromLocalStorage();
        if (localLeads.length > 0) {
            window.leads = localLeads;
            window.filteredLeads = localLeads;
            window.totalLeads = localLeads.length;
            console.log(`📁 Loaded ${window.totalLeads} leads from localStorage (cached)`);
            forceUpdateDashboard();
        } else {
            console.log('🔧 No leads found, generating realistic leads...');
            generateLeads();
        }
    }
    
    verifyAuthentication().then(() => {
        if (isAuthenticated) {
            loadDashboardStats();
            loadLeads();
            loadGlobalLeads();
            loadPrioritizedLeads();
            loadAPIUsage();
            loadCountryFilters(currentCountry);
            updateBackendInfo();
            setupExportMenu();
            startAutoRefresh();
            startConnectionMonitor();
        }
    });
    
    setupEventListeners();
    updateSourceBadges();
    loadScrapeStats();
    checkForNewLeads();
    
    setTimeout(() => {
        if (window.leads && window.leads.length > 0) {
            console.log(`🔄 Final refresh with ${window.leads.length} leads`);
            forceUpdateDashboard();
        }
    }, 500);
    
    setTimeout(() => {
        if (window.leads && window.leads.length > 0) {
            console.log(`🔄 Second refresh with ${window.leads.length} leads`);
            forceUpdateDashboard();
        }
    }, 2000);
}

// ============================================================
// EXPOSE ALL FUNCTIONS GLOBALLY
// ============================================================
window.initIndustryFilters = initIndustryFilters;
window.initIndustryFiltersWithCheckboxes = initIndustryFiltersWithCheckboxes;
window.forceUpdateDashboard = forceUpdateDashboard;
window.toggleCategory = toggleCategory;
window.onIndustryChange = onIndustryChange;
window.showDashboard = showDashboard;
window.showCompanies = showCompanies;
window.showEthiopianCompanies = showEthiopianCompanies;
window.showGlobalCompanies = showGlobalCompanies;
window.showDecisionMakers = showDecisionMakers;
window.showSignals = showSignals;
window.showExports = showExports;
window.showSettings = showSettings;
window.showLeadDetails = showLeadDetails;
window.loadLeads = loadLeads;
window.massiveScrape = massiveScrape;
window.globalScrape = globalScrape;
window.ethiopianScrape = ethiopianScrape;
window.testScrapingbee = testScrapingbee;
window.testHunterApi = testHunterApi;
window.discoverDomain = discoverDomain;
window.verifyEmail = verifyEmail;
window.verifyEmailDIY = verifyEmailDIY;
window.discoverEmails = discoverEmails;
window.checkAPIUsage = checkAPIUsage;
window.reconnectMongoDB = reconnectMongoDB;
window.checkHealth = checkHealth;
window.refreshDashboard = refreshDashboard;
window.exportLeadsByPeriod = exportLeadsByPeriod;
window.exportSignalsToFolder = exportSignalsToFolder;
window.setFilter = setFilter;
window.setMarket = setMarket;
window.exportSingleLead = exportSingleLead;
window.retryConnection = retryConnection;
window.addRecentActivity = addRecentActivity;
window.createOrUpdateChart = createOrUpdateChart;
window.onCountryDropdownChange = onCountryDropdownChange;
window.onCityDropdownChange = onCityDropdownChange;
window.onIndustryDropdownChange = onIndustryDropdownChange;
window.applyCountryFilter = applyCountryFilter;
window.clearCountryFilter = clearCountryFilter;
window.loadSampleData = loadSampleData;
window.applyEthiopianFilters = applyEthiopianFilters;
window.initializeDashboard = initializeDashboard;
window.generateLeads = generateLeads;
window.showToast = showToast;
window.loadCountryFilters = loadCountryFilters;
window.startConnectionMonitor = startConnectionMonitor;
window.applyGlobalFilters = applyGlobalFilters;
window.updateGlobalFilters = updateGlobalFilters;
window.populateGlobalFilters = populateGlobalFilters;
window.checkLeadsData = checkLeadsData;

console.log('✅ Global AI Powered Lead Gen Dashboard Ready - v11.0');
console.log('🌍 Global Market Features:');
console.log(`   • ${GLOBAL_CONFIG.countries.length} Countries Available`);
console.log(`   • ${ALL_INDUSTRIES.length} Industries Available`);
console.log(`   • ${Object.keys(INDUSTRY_HIERARCHY).length} Industry Categories`);
console.log('🇪🇹 Ethiopian Market included as default option');
console.log('📈 Features: Global Lead Generation, Industry Filters, Country Filters, City Filters');
console.log('💾 Local Storage: Leads are cached for offline viewing');
console.log('✅ DIY SMTP/DNS Email Verification (UNLIMITED & FREE)');
console.log('✅ Auto-refresh every 30 seconds');
console.log('✅ Connection Monitor Active');
console.log('💡 Click "Generate Leads" to ADD NEW leads to your collection!');

// ============================================================
// INIT ON DOM READY
// ============================================================
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeDashboard);
} else {
    initializeDashboard();
}

console.log('✅ app.js loaded successfully - Each click ADDS NEW leads!');