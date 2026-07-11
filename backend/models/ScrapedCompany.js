const mongoose = require('mongoose');

const scrapedCompanySchema = new mongoose.Schema({
    // Basic Info
    name: { type: String, required: true, index: true },
    website: { type: String, required: true, unique: true },
    domain: { type: String, index: true },
    
    // Company Details
    description: String,
    industry: { type: String, index: true },
    foundedYear: Number,
    employeesRange: String,
    revenueRange: String,
    headquarters: String,
    
    // Contact Info
    email: String,
    phone: String,
    linkedinUrl: String,
    crunchbaseUrl: String,
    
    // Financials
    fundingAmount: Number,
    fundingStage: String,
    lastFundingDate: Date,
    
    // Tech Stack
    technologies: [String],
    techStack: [{
        category: String,
        technologies: [String]
    }],
    
    // Team
    teamSize: Number,
    keyPeople: [{
        name: String,
        role: String,
        linkedin: String
    }],
    
    // Social & Metrics
    socialMedia: {
        twitter: String,
        facebook: String,
        instagram: String
    },
    alexaRank: Number,
    monthlyVisitors: Number,
    
    // Source Tracking
    sources: [{
        name: String,  // 'LinkedIn', 'Crunchbase', 'BuiltWith', etc.
        url: String,
        scrapedAt: Date,
        confidence: Number  // 0-100%
    }],
    
    // Data Quality
    dataQuality: {
        completeness: Number,
        accuracy: Number,
        freshness: Number
    },
    
    // Status
    status: {
        type: String,
        enum: ['pending', 'verified', 'rejected', 'duplicate'],
        default: 'pending'
    },
    
    // Metadata
    scrapedAt: { type: Date, default: Date.now },
    lastUpdated: Date,
    verifiedAt: Date,
    
    // Enrichment
    enrichedWithAI: Boolean,
    aiGeneratedDescription: String,
    
    // Tags for filtering
    tags: [String],
    
    // Timestamps
    createdAt: { type: Date, default: Date.now },
    updatedAt: { type: Date, default: Date.now }
}, {
    timestamps: true
});

// Indexes for faster queries
scrapedCompanySchema.index({ industry: 1, employeesRange: 1 });
scrapedCompanySchema.index({ fundingStage: 1, fundingAmount: 1 });
scrapedCompanySchema.index({ scrapedAt: -1 });
scrapedCompanySchema.index({ status: 1 });

module.exports = mongoose.model('ScrapedCompany', scrapedCompanySchema);