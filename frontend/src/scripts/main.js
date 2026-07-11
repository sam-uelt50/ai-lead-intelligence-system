// frontend/src/scripts/main.js
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Global state
let currentPage = 'dashboard';
let companiesSkip = 0;
const companiesLimit = 10;

// DOM Elements
const sections = {
    dashboard: document.getElementById('dashboard'),
    companies: document.getElementById('companies'),
    leads: document.getElementById('leads'),
    research: document.getElementById('research')
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Agency Lead Intelligence System initialized');
    
    // Setup event listeners
    setupEventListeners();
    
    // Load initial data
    loadSystemStatus();
    loadDashboardStats();
    loadPriorityLeads();
    loadCompanies();
    
    // Show dashboard by default
    showSection('dashboard');
});

// Event Listeners Setup
function setupEventListeners() {
    // Navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = this.getAttribute('href').substring(1);
            showSection(target);
        });
    });
    
    // Buttons
    document.getElementById('refreshBtn').addEventListener('click', refreshAllData);
    document.getElementById('addCompanyBtn').addEventListener('click', showAddCompanyModal);
    document.getElementById('saveCompanyBtn').addEventListener('click', saveCompany);
    document.getElementById('loadMoreCompanies').addEventListener('click', loadMoreCompanies);
    document.getElementById('searchCompaniesBtn').addEventListener('click', searchCompanies);
    
    // Search input
    document.getElementById('companySearch').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchCompanies();
        }
    });
    
    // Company filter
    document.getElementById('companyFilter').addEventListener('change', searchCompanies);
}

// Section Navigation
function showSection(sectionName) {
    // Hide all sections
    Object.values(sections).forEach(section => {
        if (section) section.style.display = 'none';
    });
    
    // Show selected section
    if (sections[sectionName]) {
        sections[sectionName].style.display = 'block';
        currentPage = sectionName;
        
        // Update navigation active state
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${sectionName}`) {
                link.classList.add('active');
            }
        });
        
        // Load section-specific data
        if (sectionName === 'companies') {
            loadCompanies();
        } else if (sectionName === 'leads') {
            loadPriorityLeads();
        }
    }
}

// API Functions
async function apiRequest(endpoint, method = 'GET', data = null) {
    const url = `${API_BASE_URL}${endpoint}`;
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        showAlert('danger', `API Error: ${error.message}`);
        throw error;
    }
}

// Dashboard Functions
async function loadSystemStatus() {
    try {
        const statusDiv = document.getElementById('systemStatus');
        
        // Check backend health
        const response = await fetch('http://localhost:8000/health');
        
        if (response.ok) {
            const data = await response.json();
            statusDiv.className = 'alert alert-success';
            statusDiv.innerHTML = `
                <i class="fas fa-check-circle me-2"></i>
                System is healthy. Database: ${data.database}
            `;
        } else {
            statusDiv.className = 'alert alert-danger';
            statusDiv.innerHTML = `
                <i class="fas fa-exclamation-circle me-2"></i>
                Backend server is not responding. Make sure the backend is running.
            `;
        }
    } catch (error) {
        const statusDiv = document.getElementById('systemStatus');
        statusDiv.className = 'alert alert-danger';
        statusDiv.innerHTML = `
            <i class="fas fa-exclamation-circle me-2"></i>
            Cannot connect to backend: ${error.message}
        `;
    }
}

async function loadDashboardStats() {
    try {
        const stats = await apiRequest('/leads/stats');
        
        // Update stats cards
        document.getElementById('totalCompanies').textContent = stats.total_companies || 0;
        document.getElementById('qualifiedLeads').textContent = stats.qualified_leads || 0;
        document.getElementById('avgScore').textContent = stats.average_score?.toFixed(1) || '0.0';
        
        // Count hot leads
        const hotLeads = stats.priority_distribution?.hot || 0;
        document.getElementById('hotLeads').textContent = hotLeads;
        
    } catch (error) {
        console.error('Failed to load dashboard stats:', error);
    }
}

// Companies Functions
async function loadCompanies() {
    try {
        const companiesTable = document.getElementById('companiesTable');
        companiesTable.innerHTML = '<tr><td colspan="7" class="text-center"><div class="spinner-border"></div></td></tr>';
        
        const priorityFilter = document.getElementById('companyFilter').value;
        const searchQuery = document.getElementById('companySearch').value;
        
        let endpoint = `/companies?skip=${companiesSkip}&limit=${companiesLimit}`;
        
        // Apply filters
        const params = [];
        if (priorityFilter) params.push(`priority=${priorityFilter}`);
        if (searchQuery) params.push(`name=${encodeURIComponent(searchQuery)}`);
        
        if (params.length > 0) {
            endpoint += `&${params.join('&')}`;
        }
        
        const companies = await apiRequest(endpoint);
        
        if (companies.length === 0) {
            companiesTable.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center text-muted py-4">
                        <i class="fas fa-building fa-2x mb-3 d-block"></i>
                        No companies found
                    </td>
                </tr>
            `;
            return;
        }
        
        let tableHTML = '';
        
        companies.forEach(company => {
            const signalsCount = company.growth_signals?.length || 0;
            const priorityClass = `badge-${company.priority}`;
            const scoreClass = getScoreClass(company.score);
            
            tableHTML += `
                <tr>
                    <td>
                        <strong>${company.name}</strong>
                        ${company.website ? `<br><small class="text-muted">${company.website}</small>` : ''}
                    </td>
                    <td>${company.industry || '-'}</td>
                    <td>${company.size || '-'}</td>
                    <td>
                        <span class="badge bg-info">${signalsCount}</span>
                        ${signalsCount > 0 ? '<i class="fas fa-bolt text-warning ms-1"></i>' : ''}
                    </td>
                    <td>
                        <span class="score-badge ${scoreClass}">
                            ${company.score}
                        </span>
                    </td>
                    <td>
                        <span class="priority-badge ${priorityClass}">
                            ${company.priority.toUpperCase()}
                        </span>
                    </td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary" onclick="viewCompanyDetails('${company._id}')">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-success ms-1" onclick="detectSignals('${company._id}')">
                            <i class="fas fa-bolt"></i>
                        </button>
                    </td>
                </tr>
            `;
        });
        
        companiesTable.innerHTML = tableHTML;
        
    } catch (error) {
        console.error('Failed to load companies:', error);
        const companiesTable = document.getElementById('companiesTable');
        companiesTable.innerHTML = `
            <tr>
                <td colspan="7" class="text-center text-danger py-4">
                    <i class="fas fa-exclamation-circle me-2"></i>
                    Failed to load companies
                </td>
            </tr>
        `;
    }
}

async function loadMoreCompanies() {
    companiesSkip += companiesLimit;
    await loadCompanies();
}

async function searchCompanies() {
    companiesSkip = 0;
    await loadCompanies();
}

// Leads Functions
async function loadPriorityLeads() {
    try {
        const leadsList = document.getElementById('leadsList');
        leadsList.innerHTML = '<div class="text-center py-5"><div class="spinner-border text-primary"></div></div>';
        
        const leads = await apiRequest('/leads/priority?limit=10');
        
        if (leads.length === 0) {
            leadsList.innerHTML = `
                <div class="text-center py-5">
                    <i class="fas fa-bullseye fa-3x text-muted mb-3"></i>
                    <h5 class="text-muted">No priority leads found</h5>
                    <p class="text-muted">Add companies to start detecting signals</p>
                </div>
            `;
            return;
        }
        
        let leadsHTML = '';
        
        leads.forEach(lead => {
            const company = lead.company;
            const signals = company.growth_signals || [];
            const signalTypes = [...new Set(signals.map(s => s.type))];
            
            leadsHTML += `
                <div class="lead-card card mb-3 ${company.priority}">
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-8">
                                <h5 class="card-title">${company.name}</h5>
                                <p class="card-text text-muted mb-2">
                                    ${company.industry || 'Unknown Industry'} • ${company.size || 'Unknown Size'}
                                </p>
                                
                                ${signals.length > 0 ? `
                                    <div class="mb-2">
                                        <strong>Growth Signals:</strong>
                                        ${signals.slice(0, 3).map(signal => `
                                            <span class="signal-badge">${signal.type}</span>
                                        `).join('')}
                                        ${signals.length > 3 ? `<span class="signal-badge">+${signals.length - 3} more</span>` : ''}
                                    </div>
                                ` : ''}
                                
                                <p class="mb-1"><strong>Why this lead:</strong> ${lead.reason}</p>
                                <p class="mb-1"><strong>Next action:</strong> ${lead.next_best_action}</p>
                            </div>
                            <div class="col-md-4 text-end">
                                <div class="mb-3">
                                    <span class="priority-badge badge-${company.priority} me-2">
                                        ${company.priority.toUpperCase()}
                                    </span>
                                    <span class="score-badge ${getScoreClass(company.score)}">
                                        ${company.score}
                                    </span>
                                </div>
                                
                                <div class="progress mb-2" style="height: 10px;">
                                    <div class="progress-bar bg-success" 
                                         style="width: ${lead.estimated_conversion_probability}%">
                                    </div>
                                </div>
                                <small class="text-muted">${lead.estimated_conversion_probability}% conversion probability</small>
                                
                                <div class="mt-3">
                                    <button class="btn btn-sm btn-primary" onclick="viewCompanyDetails('${company._id}')">
                                        <i class="fas fa-eye me-1"></i> View Details
                                    </button>
                                    <button class="btn btn-sm btn-outline-success ms-1" onclick="generateResearchBrief('${company._id}')">
                                        <i class="fas fa-search me-1"></i> Research
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });
        
        leadsList.innerHTML = leadsHTML;
        
    } catch (error) {
        console.error('Failed to load leads:', error);
        const leadsList = document.getElementById('leadsList');
        leadsList.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-circle me-2"></i>
                Failed to load leads: ${error.message}
            </div>
        `;
    }
}

// Company Management Functions
function showAddCompanyModal() {
    const modal = new bootstrap.Modal(document.getElementById('addCompanyModal'));
    modal.show();
}

async function saveCompany() {
    const companyData = {
        name: document.getElementById('companyName').value.trim(),
        website: document.getElementById('companyWebsite').value.trim(),
        industry: document.getElementById('companyIndustry').value.trim(),
        size: document.getElementById('companySize').value
    };
    
    if (!companyData.name) {
        showAlert('warning', 'Company name is required');
        return;
    }
    
    try {
        const saveBtn = document.getElementById('saveCompanyBtn');
        saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Saving...';
        saveBtn.disabled = true;
        
        const result = await apiRequest('/companies', 'POST', companyData);
        
        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('addCompanyModal'));
        modal.hide();
        
        // Reset form
        document.getElementById('companyForm').reset();
        
        // Show success message
        showAlert('success', `Company created successfully! Detected ${result.signals_detected} signals.`);
        
        // Refresh data
        refreshAllData();
        
    } catch (error) {
        showAlert('danger', `Failed to create company: ${error.message}`);
    } finally {
        const saveBtn = document.getElementById('saveCompanyBtn');
        saveBtn.innerHTML = '<i class="fas fa-save me-2"></i>Save Company';
        saveBtn.disabled = false;
    }
}

async function viewCompanyDetails(companyId) {
    try {
        const company = await apiRequest(`/companies/${companyId}`);
        
        let signalsHTML = '';
        if (company.growth_signals && company.growth_signals.length > 0) {
            signalsHTML = company.growth_signals.map(signal => `
                <div class="mb-2">
                    <strong>${signal.type.toUpperCase()}:</strong> ${signal.description}
                    <br>
                    <small class="text-muted">
                        Source: ${signal.source} • Confidence: ${signal.confidence}%
                        ${signal.detected_at ? `• Detected: ${new Date(signal.detected_at).toLocaleDateString()}` : ''}
                    </small>
                </div>
            `).join('');
        } else {
            signalsHTML = '<p class="text-muted">No growth signals detected yet.</p>';
        }
        
        let decisionMakersHTML = '';
        if (company.decision_makers && company.decision_makers.length > 0) {
            decisionMakersHTML = company.decision_makers.map(dm => `
                <div class="mb-2">
                    <strong>${dm.name}</strong> - ${dm.title}
                    ${dm.email ? `<br><small>Email: ${dm.email}</small>` : ''}
                    ${dm.linkedin ? `<br><small>LinkedIn: ${dm.linkedin}</small>` : ''}
                </div>
            `).join('');
        } else {
            decisionMakersHTML = '<p class="text-muted">No decision makers added.</p>';
        }
        
        const detailsHTML = `
            <div class="row">
                <div class="col-md-6">
                    <h6>Company Information</h6>
                    <p><strong>Name:</strong> ${company.name}</p>
                    <p><strong>Website:</strong> ${company.website || 'N/A'}</p>
                    <p><strong>Industry:</strong> ${company.industry || 'N/A'}</p>
                    <p><strong>Size:</strong> ${company.size || 'N/A'}</p>
                    <p><strong>Score:</strong> <span class="badge bg-primary">${company.score}</span></p>
                    <p><strong>Priority:</strong> <span class="priority-badge badge-${company.priority}">${company.priority.toUpperCase()}</span></p>
                </div>
                <div class="col-md-6">
                    <h6>Growth Signals</h6>
                    ${signalsHTML}
                </div>
            </div>
            <div class="row mt-3">
                <div class="col-12">
                    <h6>Decision Makers</h6>
                    ${decisionMakersHTML}
                </div>
            </div>
            ${company.research_brief ? `
                <div class="row mt-3">
                    <div class="col-12">
                        <h6>Research Brief</h6>
                        <div class="alert alert-info">
                            ${company.research_brief.replace(/\n/g, '<br>')}
                        </div>
                    </div>
                </div>
            ` : ''}
            <div class="row mt-3">
                <div class="col-12">
                    <button class="btn btn-primary" onclick="detectSignals('${company._id}')">
                        <i class="fas fa-bolt me-2"></i>Detect Signals
                    </button>
                    <button class="btn btn-success ms-2" onclick="generateResearchBrief('${company._id}')">
                        <i class="fas fa-search me-2"></i>Generate Research Brief
                    </button>
                </div>
            </div>
        `;
        
        document.getElementById('companyDetailsTitle').textContent = company.name;
        document.getElementById('companyDetailsContent').innerHTML = detailsHTML;
        
        const modal = new bootstrap.Modal(document.getElementById('companyDetailsModal'));
        modal.show();
        
    } catch (error) {
        showAlert('danger', `Failed to load company details: ${error.message}`);
    }
}

async function detectSignals(companyId) {
    try {
        showAlert('info', 'Detecting signals...');
        
        const result = await apiRequest(`/companies/${companyId}/detect-signals`, 'POST');
        
        showAlert('success', `Detected ${result.total_signals} signals. New score: ${result.new_score}`);
        
        // Refresh data
        if (currentPage === 'companies') {
            loadCompanies();
        } else if (currentPage === 'leads') {
            loadPriorityLeads();
        }
        loadDashboardStats();
        
    } catch (error) {
        showAlert('danger', `Failed to detect signals: ${error.message}`);
    }
}

async function generateResearchBrief(companyId) {
    try {
        showAlert('info', 'Generating research brief...');
        
        const result = await apiRequest(`/research/${companyId}/brief`);
        
        // Show brief in modal
        document.getElementById('companyDetailsTitle').textContent = `Research Brief: ${result.company_name}`;
        document.getElementById('companyDetailsContent').innerHTML = `
            <div class="alert alert-info">
                ${result.brief.replace(/\n/g, '<br>')}
            </div>
            <button class="btn btn-primary" onclick="viewCompanyDetails('${companyId}')">
                <i class="fas fa-arrow-left me-2"></i>Back to Company
            </button>
        `;
        
        const modal = new bootstrap.Modal(document.getElementById('companyDetailsModal'));
        modal.show();
        
    } catch (error) {
        showAlert('danger', `Failed to generate research brief: ${error.message}`);
    }
}

// Utility Functions
function refreshAllData() {
    loadSystemStatus();
    loadDashboardStats();
    
    if (currentPage === 'companies') {
        companiesSkip = 0;
        loadCompanies();
    } else if (currentPage === 'leads') {
        loadPriorityLeads();
    }
    
    showAlert('success', 'Data refreshed successfully');
}

function showAlert(type, message) {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.style.position = 'fixed';
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.style.minWidth = '300px';
    alertDiv.style.maxWidth = '500px';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Add to page
    document.body.appendChild(alertDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

function getScoreClass(score) {
    if (score >= 80) return 'score-high';
    if (score >= 60) return 'score-medium';
    return 'score-low';
}

// Make functions available globally
window.viewCompanyDetails = viewCompanyDetails;
window.detectSignals = detectSignals;
window.generateResearchBrief = generateResearchBrief;